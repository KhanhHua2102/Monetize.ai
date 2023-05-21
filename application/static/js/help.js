/*
    This function, toggleImageSection, is used to toggle the display of an image section on a web page.
    It takes a sectionNumber parameter which identifies the specific image section to toggle.

    The function first retrieves the image section element using the getElementById method and concatenates the sectionNumber to the element's ID.
    It then checks the current display style of the image section element.

    If the display style is set to 'none', indicating that the image section is hidden, the function sets the display style to 'block' to show the section.
    Otherwise, if the display style is not 'none', the function sets the display style to 'none' to hide the section.

    To use this function, you can call it with the appropriate sectionNumber as an argument.

    Example usage: toggleImageSection(1);
    This would toggle the display of the image section with the ID 'image-section-1'.

    Note: This code assumes that the image sections have unique IDs in the format 'image-section-{sectionNumber}'.
*/
function toggleImageSection(sectionNumber) {
    var imageSection = document.getElementById('image-section-' + sectionNumber);
    if (imageSection.style.display === 'none') {
        imageSection.style.display = 'block';
    } else {
        imageSection.style.display = 'none';
    }
}