// function VideoPlayerXBlock(runtime, element) {

function initializePlayer(runtime, element){
    var videoContainer = document.getElementById('video-container');
    console.log("okoko");
    console.log(videoContainer);

    if(videoContainer){
        azure_id = $("#video-container").attr("azure-id");
        almVideoPlayer.InitPlayer(videoContainer, azure_id, true, {
            controls: true,
            bigPlayButton: true
        }).then((player) => {
            console.log(player)
        }).catch((e) => {
            console.log(e);
        })
    }
}