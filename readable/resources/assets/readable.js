// Copyright 2020 Andrew Malchuk. All rights reserved.
// This project is licensed under the terms of the MIT License.

$(function() {
  // Enable tooltips everywhere:
  $("[data-toggle=\"tooltip\"]").tooltip();

  // Add filename for uploading files:
  $(".custom-file-input").on("change", function(event) {
    $(this).next(".custom-file-label").html(event.target.files[0].name);
  });
});
