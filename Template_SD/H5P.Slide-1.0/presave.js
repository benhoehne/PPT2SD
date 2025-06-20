var H5PPresave = H5PPresave || {};

/**
 * Resolve the presave logic for the content type Slide
 * Copies the slide title to metadata title
 *
 * @param {object} content
 * @param finished
 * @constructor
 */
H5PPresave['H5P.Slide'] = function (content, finished) {
  var presave = H5PEditor.Presave;
  
  // Copy the slide title to metadata if it exists
  if (content && content.title) {
    // The metadata will be set automatically by H5P core
    // We just need to pass the title in the finished callback
    finished({
      title: content.title
    });
  } else {
    // If no title is set, use a default
    finished({
      title: 'Untitled Slide'
    });
  }
}; 