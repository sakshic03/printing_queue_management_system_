
document.addEventListener("DOMContentLoaded", function () {
    console.log("Welcome to WaitLess Print!");
});

const togglePassword = document.getElementById("togglePassword");

if (togglePassword) {
    togglePassword.addEventListener("click", function () {
        const password = document.getElementById("password");

        if (password.type === "password") {
            password.type = "text";
            this.textContent = "Hide";
        } else {
            password.type = "password";
            this.textContent = "Show";
        }
    });
}

const loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const message = document.getElementById("loginMessage");
        message.textContent = "Login UI ready. Backend connection is coming soon.";
        message.style.color = "#667B62";
    });
}

// Register password visibility

function setupPasswordToggle(buttonId, inputId) {
    const button = document.getElementById(buttonId);
    const input = document.getElementById(inputId);

    if (button && input) {
        button.addEventListener("click", function () {
            if (input.type === "password") {
                input.type = "text";
                button.textContent = "Hide";
            } else {
                input.type = "password";
                button.textContent = "Show";
            }
        });
    }
}

setupPasswordToggle("toggleRegisterPassword", "registerPassword");
setupPasswordToggle("toggleConfirmPassword", "confirmPassword");


// Register form validation

const registerForm = document.getElementById("registerForm");

if (registerForm) {
    registerForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const password = document.getElementById("registerPassword").value;
        const confirmPassword = document.getElementById("confirmPassword").value;
        const message = document.getElementById("registerMessage");

        if (password !== confirmPassword) {
            message.textContent = "Passwords do not match!";
            message.style.color = "#B34C43";
            return;
        }

        message.textContent = "Registration UI ready! Backend connection is coming soon.";
        message.style.color = "#667B62";
    });
}

// Printing shop selection - frontend demo only
document.querySelectorAll(".select-shop-btn").forEach(function (button) {
    button.addEventListener("click", function () {
        const shopName = this.dataset.shop;
        const message = document.getElementById("shopMessage");

        message.textContent = shopName + " selected! Backend connection is coming soon.";

        document.querySelectorAll(".select-shop-btn").forEach(function (btn) {
            btn.textContent = "Select Shop ↗";
        });

        this.textContent = "Selected ✓";
    });
});

/* DOCUMENT UPLOAD - FRONTEND PREVIEW */

const documentFile = document.getElementById("documentFile");

if (documentFile) {
    const fileInfo = document.getElementById("fileInfo");
    const continueButton = document.getElementById("continueUpload");
    const uploadMessage = document.getElementById("uploadMessage");

    documentFile.addEventListener("change", function () {
        const file = this.files[0];

        uploadMessage.textContent = "";
        continueButton.disabled = true;

        if (!file) {
            fileInfo.textContent = "No file selected yet";
            return;
        }

        const allowedTypes = [".pdf", ".doc", ".docx"];
        const extension = file.name.substring(file.name.lastIndexOf(".")).toLowerCase();

        if (!allowedTypes.includes(extension)) {
            fileInfo.textContent = "Please select a PDF, DOC or DOCX file.";
            this.value = "";
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            fileInfo.textContent = "File size must be below 10 MB.";
            this.value = "";
            return;
        }

        fileInfo.textContent =
            file.name + " • " + (file.size / (1024 * 1024)).toFixed(2) + " MB";

        continueButton.disabled = false;
    });

    continueButton.addEventListener("click", function () {
        uploadMessage.textContent =
            "File selected! Actual upload will work after backend integration.";
    });
}

/* PRINT OPTIONS - FRONTEND PREVIEW */

const printForm = document.getElementById("printOptionsForm");

if (printForm) {
    const customPages = document.getElementById("customPages");
    const priceDisplay = document.getElementById("estimatedPrice");

    function updatePrice() {
        const type = document.querySelector('input[name="printType"]:checked').value;
        const copies = Number(document.getElementById("copies").value) || 1;
        const rate = type === "Colour" ? 5 : 2;

        priceDisplay.textContent = "₹" + (rate * copies);
    }

    document.querySelectorAll('input[name="printType"]').forEach(input => {
        input.addEventListener("change", updatePrice);
    });

    document.getElementById("copies").addEventListener("input", updatePrice);

    document.querySelectorAll('input[name="pageRange"]').forEach(input => {
        input.addEventListener("change", function () {
            customPages.style.display =
                this.value === "Custom Pages" ? "block" : "none";
        });
    });

    printForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const pages = document.querySelector('input[name="pageRange"]:checked').value;

        if (pages === "Custom Pages" && !customPages.value.trim()) {
            alert("Please enter your custom page numbers.");
            return;
        }

        document.getElementById("optionsMessage").textContent =
            "Print options selected! Backend connection is coming soon.";
    });
}

/* TRACK ORDER - FRONTEND DEMO */
const trackForm = document.getElementById("trackForm");

if (trackForm) {
    trackForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const token = document.getElementById("tokenInput").value.trim().toUpperCase();

        if (!token) return;

        document.getElementById("shownToken").textContent = token;
        document.getElementById("trackingResult").hidden = false;
    });
}

/* ADMIN STATUS - FRONTEND DEMO */
document.querySelectorAll(".order-status").forEach(function (select) {
    select.addEventListener("change", function () {
        const message = document.getElementById("adminMessage");

        if (message) {
            message.textContent =
                "Demo status changed to: " + this.value +
                ". Save to database after backend integration.";
        }
    });
});