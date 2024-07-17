function AzureVideoplayerEditBlock(runtime, element) {
  $(element).find('.save-button').bind('click', function() {
    var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
    var data = {
      azure_video_name: $(element).find('input[name=azure_video_name]').val(),
    };
    runtime.notify('save', {state: 'start'});
    $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
      if (response.errors.length > 0) {
        response.errors.forEach(function (error) {
          runtime.notify("error", {
            message: error,
            title: "Azure Video Component save error",
          });
        });
      } else {
        runtime.notify('save', {state: 'end'});
      }
    });
  });

  $(element).find('.cancel-button').bind('click', function() {
    runtime.notify('cancel', {});
  });
}