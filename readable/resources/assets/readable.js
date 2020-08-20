// Copyright 2020 Andrew Malchuk. All rights reserved.
// This project is licensed under the terms of the MIT License.

$(function() {
  // Enable tooltips everywhere:
  $("[data-toggle=\"tooltip\"]").tooltip();

  // Add filename for uploading files:
  $(".custom-file-input").on("change", function(event) {
    var file_input = $(this);
    var name = event.target.files[0].name;
    file_input.next(".custom-file-label").html(name);
  });

  // Set the width of a progress bar dynamically:
  $(".progress-bar").each(function() {
    var progress_bar = $(this);
    var width = Math.max(20.0, Math.min(progress_bar.attr("aria-valuenow"), 100.0));
    progress_bar.width(`${width}%`);
  });
});
