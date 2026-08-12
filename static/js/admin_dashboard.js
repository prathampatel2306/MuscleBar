document.addEventListener("DOMContentLoaded", function () {

    /* =========================
       KPI CARD HOVER
    ========================= */

    const kpiCards = document.querySelectorAll(".kpi-card");

    kpiCards.forEach(card => {

        card.addEventListener("mouseenter", () => {
            card.style.transform = "translateY(-4px)";
            card.style.borderColor = "var(--primary)";
        });

        card.addEventListener("mouseleave", () => {
            card.style.transform = "translateY(0)";
            card.style.borderColor = "var(--outline-variant)";
        });

    });


    /* =========================
       REVENUE DATA
    ========================= */

    const revenueElement =
        document.getElementById("revenue-data");

    if (!revenueElement) {
        return;
    }

    const revenueData = JSON.parse(
        revenueElement.dataset.revenue
    );


    /* =========================
       CHART ELEMENTS
    ========================= */

    const line =
        document.getElementById("revenue-line");

    const area =
        document.getElementById("revenue-area");

    const pointsGroup =
        document.getElementById("revenue-points");

    const yAxisLabels =
        document.getElementById("y-axis-labels");


    if (
        !line ||
        !area ||
        !pointsGroup ||
        !yAxisLabels
    ) {
        return;
    }


    /* =========================
       VALID DATA
    ========================= */

    const validData = revenueData
        .map((value, index) => ({
            value: value,
            index: index
        }))
        .filter(item => item.value !== null);


    if (validData.length === 0) {
        return;
    }


    /* =========================
       DYNAMIC Y AXIS
    ========================= */

    const highestRevenue = Math.max(
        ...validData.map(item => item.value),
        0
    );

    const yAxisMax =
        Math.ceil(highestRevenue / 25000) * 25000 || 25000;


    /* =========================
       Y AXIS LABELS
    ========================= */

    yAxisLabels.innerHTML = "";

    const numberOfSteps = 4;

    for (let i = numberOfSteps; i >= 0; i--) {

        const value =
            (yAxisMax / numberOfSteps) * i;

        const label =
            document.createElement("span");

        label.textContent =
            "₹" +
            Math.round(value).toLocaleString("en-IN");

        yAxisLabels.appendChild(label);
    }


    /* =========================
       CHART COORDINATES
    ========================= */

    const chartWidth = 1000;
    const chartHeight = 350;

    /*
       These control the horizontal
       position of the first and last point.
    */

    const chartLeft = 25;
    const chartRight = 925;


    /* =========================
       CREATE POINTS
    ========================= */

    const points = validData.map(item => {

        const x =
            chartLeft +
            (item.index / 11) *
            (chartRight - chartLeft);

        const y =
            chartHeight -
            (item.value / yAxisMax) * 300;

        return {
            x: x,
            y: y,
            value: item.value,
            index: item.index
        };

    });


    /* =========================
       REVENUE LINE
    ========================= */

    const pathData = points
        .map((point, index) => {

            const command =
                index === 0 ? "M" : "L";

            return `${command}${point.x},${point.y}`;

        })
        .join(" ");


    line.setAttribute(
        "d",
        pathData
    );


    /* =========================
       AREA UNDER LINE
    ========================= */

    const firstPoint =
        points[0];

    const lastPoint =
        points[points.length - 1];

    const areaPath =
        pathData +
        ` L${lastPoint.x},${chartHeight}` +
        ` L${firstPoint.x},${chartHeight} Z`;


    area.setAttribute(
        "d",
        areaPath
    );


    /* =========================
       POINTS
    ========================= */

    pointsGroup.innerHTML = "";

    points.forEach(point => {

        const circle =
            document.createElementNS(
                "http://www.w3.org/2000/svg",
                "circle"
            );

        circle.setAttribute(
            "cx",
            point.x
        );

        circle.setAttribute(
            "cy",
            point.y
        );

        circle.setAttribute(
            "r",
            "6"
        );

        circle.setAttribute(
            "fill",
            "#ffb59c"
        );

        pointsGroup.appendChild(circle);

    });


    /* =========================
       MONTH LABELS
    ========================= */

    /*
       IMPORTANT:
       The month labels are now inside
       the same .chart-area as the SVG.

       Therefore we can use the EXACT
       same X calculation as the graph.
    */

    const monthLabels =
        document.querySelectorAll(
            "#month-labels span"
        );

    monthLabels.forEach((label, index) => {

        const x =
            chartLeft +
            (index / 11) *
            (chartRight - chartLeft);

        label.style.position = "absolute";

        label.style.left =
            `${x / 10}%`;

        label.style.transform =
            "translateX(-50%)";

    });


    /* =========================
       POINT PULSE
    ========================= */

    setInterval(() => {

        const dots =
            document.querySelectorAll(
                "#revenue-points circle"
            );

        dots.forEach(dot => {

            const currentR =
                parseFloat(
                    dot.getAttribute("r")
                );

            const targetR =
                currentR === 6 ? 7 : 6;

            dot.style.transition =
                "r 0.5s ease-in-out";

            dot.setAttribute(
                "r",
                targetR
            );

        });

    }, 1200);

});

/* =========================
   MEMBERSHIP DISTRIBUTION
========================= */

const membershipElement =
    document.getElementById("membership-data");

if (membershipElement) {

    const membershipData = JSON.parse(
        membershipElement.dataset.distribution
    );

    const donutSegments =
        document.querySelectorAll(".donut-segment");

    const circumference =
        2 * Math.PI * 40;

    let offset = 0;

    membershipData.forEach((item, index) => {

        const segment =
            donutSegments[index];

        if (!segment) {
            return;
        }

        const percentage =
            Number(item.percentage);

        const length =
            (percentage / 100) * circumference;

        segment.setAttribute(
            "stroke-dasharray",
            `${length} ${circumference}`
        );

        segment.setAttribute(
            "stroke-dashoffset",
            -offset
        );

        offset += length;

    });

    /* =========================================
   MEMBER GROWTH
========================================= */

const growthColumns =
    document.querySelectorAll(".growth-column");

if (growthColumns.length > 0) {

    const counts =
        Array.from(growthColumns).map(column => {

            return Number(
                column.dataset.count
            ) || 0;

        });

    const maxCount =
        Math.max(...counts, 0);


    growthColumns.forEach((column, index) => {

        const count =
            counts[index];

        const bar =
            column.querySelector(".growth-bar");

        const value =
            column.querySelector(".growth-value");


        /*
         * Height available for bars.
         *
         * 50px is reserved for
         * the X-axis/year labels.
         */

        const maxBarHeight = 220;


        let barHeight = 0;


        if (maxCount > 0) {

            barHeight =
                (count / maxCount)
                * maxBarHeight;

        }


        /* =========================
           BAR HEIGHT
        ========================= */

        bar.style.height =
            `${barHeight}px`;


        /* =========================
           VALUE POSITION
        ========================= */

        /*
         * Zero values stay near the
         * bottom of the chart.
         *
         * Non-zero values sit above
         * their respective bar.
         */

        if (count === 0) {

            value.style.bottom =
                "62px";

        } else {

            value.style.bottom =
                `${barHeight + 50}px`;

        }

    });

}
}

/* =========================================
   DELETE MEMBER CONFIRMATION
========================================= */

const deleteModal =
    document.getElementById("deleteMemberModal");

const deleteNoBtn =
    document.getElementById("deleteNoBtn");

const deleteYesBtn =
    document.getElementById("deleteYesBtn");

let selectedDeleteForm = null;


/* Open modal */
document.querySelectorAll(".delete-member-form").forEach(form => {

    form.addEventListener("submit", function (event) {

        event.preventDefault();

        selectedDeleteForm = form;

        deleteModal.classList.add("show");

    });

});


/* No */
deleteNoBtn.addEventListener("click", function () {

    selectedDeleteForm = null;

    deleteModal.classList.remove("show");

});


/* Yes */
deleteYesBtn.addEventListener("click", function () {

    if (selectedDeleteForm) {

        deleteModal.classList.remove("show");

        selectedDeleteForm.submit();

    }

    selectedDeleteForm = null;

});


/* Click outside modal */
deleteModal.addEventListener("click", function (event) {

    if (event.target === deleteModal) {

        selectedDeleteForm = null;

        deleteModal.classList.remove("show");

    }

});


/* Escape key */
document.addEventListener("keydown", function (event) {

    if (event.key === "Escape") {

        selectedDeleteForm = null;

        deleteModal.classList.remove("show");

    }

});

