function binaryToDataURL(binaryData) {
    var base64String = window.btoa(String.fromCharCode.apply(null, binaryData));
    return "data:image/jpeg;base64," + base64String;
  }