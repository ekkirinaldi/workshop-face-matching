document.addEventListener('DOMContentLoaded', function() {
    const image1Input = document.getElementById('image1');
    const image2Input = document.getElementById('image2');
    const preview1 = document.getElementById('preview1');
    const preview2 = document.getElementById('preview2');
    const compareBtn = document.getElementById('compareBtn');
    const resultDiv = document.getElementById('result');
    const similaritySpan = document.getElementById('similarity');
    const errorDiv = document.getElementById('error');

    let image1Base64 = null;
    let image2Base64 = null;

    function handleImageUpload(input, preview) {
        return function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                    return e.target.result;
                };
                reader.readAsDataURL(file);
            }
        };
    }

    image1Input.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview1.src = e.target.result;
                preview1.style.display = 'block';
                image1Base64 = e.target.result;
                updateCompareButton();
            };
            reader.readAsDataURL(file);
        }
    });

    image2Input.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview2.src = e.target.result;
                preview2.style.display = 'block';
                image2Base64 = e.target.result;
                updateCompareButton();
            };
            reader.readAsDataURL(file);
        }
    });

    function updateCompareButton() {
        compareBtn.disabled = !(image1Base64 && image2Base64);
    }

    compareBtn.addEventListener('click', async function() {
        try {
            compareBtn.disabled = true;
            compareBtn.textContent = 'Comparing...';
            errorDiv.style.display = 'none';

            const response = await fetch('/api/compare', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image1: image1Base64,
                    image2: image2Base64
                })
            });

            const data = await response.json();

            if (response.ok) {
                similaritySpan.textContent = data.similarity;
                resultDiv.style.display = 'block';
            } else {
                throw new Error(data.error || 'Failed to compare faces');
            }
        } catch (error) {
            errorDiv.textContent = error.message;
            errorDiv.style.display = 'block';
        } finally {
            compareBtn.disabled = false;
            compareBtn.textContent = 'Compare Faces';
        }
    });
}); 