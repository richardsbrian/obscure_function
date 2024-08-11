// scripts.js

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;

    // Hide all tab contents
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Remove the active class from all tabs
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab and add an active class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

function openBottomTab(evt, tabName) {
    var i, tabcontent, tablinks;

    // Hide all bottom tab contents
    tabcontent = document.getElementsByClassName("bottom-tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Remove the active class from all bottom tabs
    tablinks = document.getElementsByClassName("bottom-tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current bottom tab and add an active class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

function startSpinner() {
    document.querySelector('.spinner').style.display = 'block';
}

function stopSpinner() {
    document.querySelector('.spinner').style.display = 'none';
}

// Open the RebuiltResponse tab by default on top
document.getElementsByClassName('tablinks')[2].click();

// Open the PromptInput tab by default on bottom
document.getElementsByClassName('bottom-tablinks')[0].click();

document.getElementById('anonymizeBtn').addEventListener('click', function () {
    const code = document.getElementById('code').value;
    const prompt = document.getElementById('prompt').value;

    startSpinner();

    fetch('/anonymize_and_send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `code=${encodeURIComponent(code)}&prompt=${encodeURIComponent(prompt)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            document.getElementById('anonymizedResult').textContent = data.anonymized;
            document.getElementById('responseResult').textContent = data.response;
            document.getElementById('rebuiltResult').textContent = data.rebuilt_response;
        }
        stopSpinner();
    })
    .catch(error => {
        console.error('Error:', error);
        stopSpinner();
    });
});
