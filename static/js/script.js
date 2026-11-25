/**
 * PlagScan Interactive Frontend Script
 * Handles:
 * - Drag and drop file upload
 * - File selection & clear
 * - Mode toggle (Upload vs Textarea)
 * - 1-Click sample document loader
 * - Form submission state
 */

function toggleInputMode(docPrefix, mode) {
    const uploadZone = document.getElementById(`${docPrefix}_upload_zone`);
    const textZone = document.getElementById(`${docPrefix}_text_zone`);
    const parentCard = uploadZone.closest('.glass-card');
    const buttons = parentCard.querySelectorAll('.btn-mode');

    buttons.forEach(btn => btn.classList.remove('active'));

    if (mode === 'upload') {
        buttons[0].classList.add('active');
        uploadZone.classList.remove('d-none');
        textZone.classList.add('d-none');
    } else {
        buttons[1].classList.add('active');
        uploadZone.classList.add('d-none');
        textZone.classList.remove('d-none');
    }
}

function handleFileSelected(input, docPrefix) {
    const badge = document.getElementById(`${docPrefix}_file_badge`);
    const nameDisplay = document.getElementById(`${docPrefix}_file_name`);

    if (input.files && input.files[0]) {
        const file = input.files[0];
        const sizeKb = (file.size / 1024).toFixed(1);
        nameDisplay.textContent = `${file.name} (${sizeKb} KB)`;
        badge.classList.remove('d-none');
    }
}

function clearFile(docPrefix) {
    const input = document.getElementById(`${docPrefix}_file`);
    const badge = document.getElementById(`${docPrefix}_file_badge`);
    const nameDisplay = document.getElementById(`${docPrefix}_file_name`);

    input.value = "";
    nameDisplay.textContent = "";
    badge.classList.add('d-none');
}

function loadSample(sampleId) {
    fetch(`/samples/${sampleId}`)
        .then(response => response.json())
        .then(data => {
            if (data.doc1 && data.doc2) {
                // Switch both to text mode
                toggleInputMode('doc1', 'text');
                toggleInputMode('doc2', 'text');

                // Populate textareas
                document.getElementById('doc1_text').value = data.doc1;
                document.getElementById('doc2_text').value = data.doc2;

                // Smooth scroll to comparison section
                document.getElementById('comparison-section').scrollIntoView({ behavior: 'smooth' });
            }
        })
        .catch(err => console.error("Error loading sample:", err));
}

// Drag and drop listeners
document.addEventListener('DOMContentLoaded', () => {
    ['doc1', 'doc2'].forEach(prefix => {
        const zone = document.getElementById(`${prefix}_upload_zone`);
        const input = document.getElementById(`${prefix}_file`);

        if (zone && input) {
            ['dragenter', 'dragover'].forEach(eventName => {
                zone.addEventListener(eventName, (e) => {
                    e.preventDefault();
                    zone.classList.add('dragover');
                }, false);
            });

            ['dragleave', 'drop'].forEach(eventName => {
                zone.addEventListener(eventName, (e) => {
                    e.preventDefault();
                    zone.classList.remove('dragover');
                }, false);
            });

            zone.addEventListener('drop', (e) => {
                if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
                    input.files = e.dataTransfer.files;
                    handleFileSelected(input, prefix);
                }
            });
        }
    });

    // Form submit loading spinner
    const compareForm = document.getElementById('compareForm');
    const compareBtn = document.getElementById('compareBtn');
    if (compareForm && compareBtn) {
        compareForm.addEventListener('submit', () => {
            compareBtn.disabled = true;
            compareBtn.innerHTML = `
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                <span>Executing Algorithm & Comparing...</span>
            `;
        });
    }
});
