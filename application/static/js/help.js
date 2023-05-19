function toggleImageSection(sectionNumber) {
    var imageSection = document.getElementById('image-section-' + sectionNumber);
    if (imageSection.style.display === 'none') {
      imageSection.style.display = 'block';
    } else {
      imageSection.style.display = 'none';
    }
  }