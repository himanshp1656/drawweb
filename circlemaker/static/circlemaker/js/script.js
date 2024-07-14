// const canvas = document.getElementById('drawingCanvas');
// const context = canvas.getContext('2d');
// const circularityDisplay = document.getElementById('circularity');

// canvas.width = window.innerWidth * 0.8;
// canvas.height = window.innerHeight * 0.8;

// let drawing = false;
// let points = [];

// const dot = {
//     x: canvas.width / 2,
//     y: canvas.height / 2,
//     radius: 5
// };

// // Draw the initial dot
// drawDot();

// canvas.addEventListener('mousedown', startDrawing);
// canvas.addEventListener('mouseup', stopDrawing);
// canvas.addEventListener('mousemove', draw);

// canvas.addEventListener('touchstart', startDrawing);
// canvas.addEventListener('touchend', stopDrawing);
// canvas.addEventListener('touchmove', draw);

// function startDrawing(event) {
//     drawing = true;
//     points = [];
//     context.clearRect(0, 0, canvas.width, canvas.height);
//     drawDot();
//     event.preventDefault();
// }

// function stopDrawing() {
//     drawing = false;
// }

// function draw(event) {
//     if (!drawing) return;

//     const rect = canvas.getBoundingClientRect();
//     let x, y;

//     if (event.type === 'mousemove') {
//         x = event.clientX - rect.left;
//         y = event.clientY - rect.top;
//     } else if (event.type === 'touchmove') {
//         const touch = event.touches[0];
//         x = touch.clientX - rect.left;
//         y = touch.clientY - rect.top;
//     }

//     context.lineWidth = 2;
//     context.lineCap = 'round';
//     context.strokeStyle = 'red';

//     context.lineTo(x, y);
//     context.stroke();
//     points.push({ x, y });

//     calculateCircularity(); // Calculate circularity in real-time

//     event.preventDefault();
// }

// function drawDot() {
//     context.beginPath();
//     context.arc(dot.x, dot.y, dot.radius, 0, Math.PI * 2, true);
//     context.fillStyle = 'red';
//     context.fill();
// }

// function calculateCircularity() {
//     if (points.length < 2) {
//         circularityDisplay.innerText = "Circularity: N/A";
//         return;
//     }

//     // Calculate area using the shoelace formula
//     let area = 0;
//     for (let i = 0; i < points.length; i++) {
//         const j = (i + 1) % points.length;
//         area += points[i].x * points[j].y - points[j].x * points[i].y;
//     }
//     area = Math.abs(area) / 2;

//     // Calculate perimeter
//     let perimeter = 0;
//     for (let i = 1; i < points.length; i++) {
//         const dx = points[i].x - points[i - 1].x;
//         const dy = points[i].y - points[i - 1].y;
//         perimeter += Math.sqrt(dx * dx + dy * dy);
//     }

//     // Close the shape if it's not closed
//     if (points.length > 2) {
//         const dx = points[0].x - points[points.length - 1].x;
//         const dy = points[0].y - points[points.length - 1].y;
//         perimeter += Math.sqrt(dx * dx + dy * dy);
//     }

//     // Calculate circularity
//     const circularity = (4 * Math.PI * area) / (perimeter * perimeter);

//     // Clamp circularity between 0 and 1 and convert to percentage
//     const circularityPercentage = Math.min(circularity * 100, 100);

//     circularityDisplay.innerText = `Circularity: ${circularityPercentage.toFixed(2)}%`;
// }







const canvas = document.getElementById('drawingCanvas');
const context = canvas.getContext('2d');
const circularityDisplay = document.getElementById('circularity');

canvas.width = window.innerWidth * 0.8;
canvas.height = window.innerHeight * 0.8;

let drawing = false;
let points = [];
let previousCircularity = 0;

const dot = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    radius: 5
};

// Draw the initial dot
drawDot();

canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mousemove', draw);

canvas.addEventListener('touchstart', startDrawing);
canvas.addEventListener('touchend', stopDrawing);
canvas.addEventListener('touchmove', draw);

function startDrawing(event) {
    drawing = true;
    points = [];
    context.clearRect(0, 0, canvas.width, canvas.height);
    drawDot();
    event.preventDefault();
}

function stopDrawing() {
    drawing = false;
}

function draw(event) {
    if (!drawing) return;

    const rect = canvas.getBoundingClientRect();
    let x, y;

    if (event.type === 'mousemove') {
        x = event.clientX - rect.left;
        y = event.clientY - rect.top;
    } else if (event.type === 'touchmove') {
        const touch = event.touches[0];
        x = touch.clientX - rect.left;
        y = touch.clientY - rect.top;
    }

    points.push({ x, y });

    // Calculate circularity
    const circularity = calculateCircularity();

    // Draw segments based on circularity change
    if (points.length > 1) {
        const lastPoint = points[points.length - 2];

        context.beginPath();
        context.moveTo(lastPoint.x, lastPoint.y);

        // Set line width
        context.lineWidth = 5; // Increased line width
        context.lineCap = 'round';
        context.strokeStyle = circularity > previousCircularity ? 'green' : 'red';
        context.lineTo(x, y);
        context.stroke();
    }

    // Update previous circularity
    previousCircularity = circularity;

    // Update circularity display
    circularityDisplay.innerText = `Circularity: ${circularity.toFixed(2)}%`;

    event.preventDefault();
}

function drawDot() {
    context.beginPath();
    context.arc(dot.x, dot.y, dot.radius, 0, Math.PI * 2, true);
    context.fillStyle = 'red';
    context.fill();
}

function calculateCircularity() {
    if (points.length < 2) {
        circularityDisplay.innerText = "Circularity: N/A";
        return 0; // Return 0 when not enough points
    }

    // Calculate area using the shoelace formula
    let area = 0;
    for (let i = 0; i < points.length; i++) {
        const j = (i + 1) % points.length;
        area += points[i].x * points[j].y - points[j].x * points[i].y;
    }
    area = Math.abs(area) / 2;

    // Calculate perimeter
    let perimeter = 0;
    for (let i = 1; i < points.length; i++) {
        const dx = points[i].x - points[i - 1].x;
        const dy = points[i].y - points[i - 1].y;
        perimeter += Math.sqrt(dx * dx + dy * dy);
    }

    // Close the shape if it's not closed
    if (points.length > 2) {
        const dx = points[0].x - points[points.length - 1].x;
        const dy = points[0].y - points[points.length - 1].y;
        perimeter += Math.sqrt(dx * dx + dy * dy);
    }

    // Calculate circularity
    const circularity = (4 * Math.PI * area) / (perimeter * perimeter);

    // Clamp circularity between 0 and 1 and convert to percentage
    return Math.min(circularity * 100, 100);
}