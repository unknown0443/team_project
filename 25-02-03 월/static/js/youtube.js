var players = {};
var youtubeAPIReady = false;

function onYouTubeIframeAPIReady() {
    youtubeAPIReady = true;
    console.log("✅ [YouTube API] IFrame API 로드 완료");

    document.querySelectorAll(".video-container").forEach(container => {
        let videoId = container.getAttribute("data-video-id");
        createPlayer(videoId);
    });
}

function createPlayer(videoId) {
    let container = document.querySelector(`[data-video-id='${videoId}']`);
    if (!container) {
        console.log(`❌ [YouTube] video-${videoId} 컨테이너를 찾을 수 없음`);
        return;
    }

    container.innerHTML = "";

    let iframe = document.createElement("iframe");
    iframe.setAttribute("id", `player-${videoId}`);
    iframe.setAttribute("width", "560");
    iframe.setAttribute("height", "315");
    iframe.setAttribute("src", `https://www.youtube.com/embed/${videoId}?enablejsapi=1`);
    iframe.setAttribute("frameborder", "0");
    iframe.setAttribute("allowfullscreen", "");

    container.appendChild(iframe);

    players[videoId] = new YT.Player(`player-${videoId}`, {
        events: {
            'onReady': function(event) {
                console.log(`✅ [YouTube API] Player ready for video: ${videoId}`);
            }
        }
    });

    console.log(`🎬 [YouTube] 새로운 플레이어 생성: ${videoId}`);
}

document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".video-container").forEach(container => {
        let videoId = container.getAttribute("data-video-id");
        createPlayer(videoId);
    });

    document.querySelectorAll(".timestamp").forEach(ts => {
        ts.addEventListener("click", function(event) {
            let videoId = event.target.dataset.video;
            let seconds = parseFloat(event.target.dataset.seconds);

            console.log(`🎯 [JavaScript] 클릭한 타임스탬프: videoId=${videoId}, seconds=${seconds}`);

            if (!players[videoId]) {
                console.log(`⚠️ [JavaScript] 플레이어가 존재하지 않음. 새로 생성.`);
                createPlayer(videoId);
                
                setTimeout(() => {
                    if (players[videoId]) {
                        console.log(`✅ [JavaScript] 지연 후 seekTo 실행: ${seconds}초`);
                        players[videoId].seekTo(seconds, true);
                        players[videoId].playVideo();
                    } else {
                        console.log(`❌ [JavaScript] 여전히 seekTo() 실행 불가: videoId=${videoId}`);
                    }
                }, 1000);
                return;
            }

            console.log(`🔹 [JavaScript] seekTo 실행: ${seconds}초로 이동`);
            players[videoId].seekTo(seconds, true);
            players[videoId].playVideo();
        });
    });
});

