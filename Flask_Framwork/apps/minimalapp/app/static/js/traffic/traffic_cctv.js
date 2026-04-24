const regionPresets = {
  seoul: {
    minX: "126.70",
    maxX: "127.20",
    minY: "37.30",
    maxY: "37.70"
  },
  suwon: {
    minX: "126.90",
    maxX: "127.15",
    minY: "37.15",
    maxY: "37.35"
  },
  daejeon: {
    minX: "127.25",
    maxX: "127.55",
    minY: "36.20",
    maxY: "36.45"
  },
  busan: {
    minX: "128.90",
    maxX: "129.25",
    minY: "35.05",
    maxY: "35.30"
  }
};

let hlsInstance = null;

function getElement(id) {
  return document.getElementById(id);
}

function setLoading(isLoading) {
  const loading = getElement("traffic-loading");
  if (loading) {
    loading.style.display = isLoading ? "block" : "none";
  }
}

function showError(message) {
  const errorBox = getElement("traffic-error");

  if (!errorBox) {
    return;
  }

  if (!message) {
    errorBox.style.display = "none";
    errorBox.textContent = "";
    return;
  }

  errorBox.style.display = "block";
  errorBox.textContent = message;
}

function applyRegionPreset(regionKey) {
  const preset = regionPresets[regionKey];

  if (!preset) {
    return;
  }

  getElement("minX").value = preset.minX;
  getElement("maxX").value = preset.maxX;
  getElement("minY").value = preset.minY;
  getElement("maxY").value = preset.maxY;
}

async function loadCctvList() {
  const roadType = getElement("roadType").value;
  const cctvType = getElement("cctvType").value;

  const minX = getElement("minX").value.trim();
  const maxX = getElement("maxX").value.trim();
  const minY = getElement("minY").value.trim();
  const maxY = getElement("maxY").value.trim();

  const listBox = getElement("traffic-cctv-list");
  const countBox = getElement("traffic-count");

  listBox.innerHTML = "";
  countBox.textContent = "조회 중입니다.";

  showError("");
  setLoading(true);

  const query = new URLSearchParams({
    roadType,
    cctvType,
    minX,
    maxX,
    minY,
    maxY
  });

  try {
    const response = await fetch(`/traffic/api/cctv?${query.toString()}`);
    const result = await response.json();

    console.log("[CCTV API RESULT]", result);

    if (!response.ok || !result.success) {
      throw new Error(result.message || "CCTV 목록 조회에 실패했습니다.");
    }

    const cctvList = result.data || [];

    countBox.textContent = `총 ${cctvList.length}개의 CCTV가 조회되었습니다.`;

    renderCctvList(cctvList);

  } catch (error) {
    console.error("[TRAFFIC CCTV ERROR]", error);
    showError(error.message || "CCTV 목록 조회 중 오류가 발생했습니다.");
    countBox.textContent = "조회 실패";
  } finally {
    setLoading(false);
  }
}

function renderCctvList(cctvList) {
  const listBox = getElement("traffic-cctv-list");

  if (!cctvList.length) {
    listBox.innerHTML = `
      <div class="empty-box">
        <p>조회된 CCTV가 없습니다. 좌표 범위를 넓혀보세요.</p>
      </div>
    `;
    return;
  }

  cctvList.forEach((cctv) => {
    const item = document.createElement("div");
    item.className = "traffic-cctv-item";

    const hasUrl = Boolean(cctv.url);

    item.innerHTML = `
      <h4>${escapeHtml(cctv.name || "이름 없음")}</h4>
      <p>좌표: ${escapeHtml(cctv.coordy || "-")}, ${escapeHtml(cctv.coordx || "-")}</p>
      <p>형식: ${escapeHtml(cctv.format || "-")}</p>
      <p>해상도: ${escapeHtml(cctv.resolution || "-")}</p>
      <p>생성시각: ${escapeHtml(cctv.file_create_time || "-")}</p>
      <p class="traffic-url-text">URL: ${hasUrl ? "있음" : "없음"}</p>

      <div class="traffic-cctv-actions">
        <button type="button" class="btn btn-primary btn-sm play-cctv-btn" ${hasUrl ? "" : "disabled"}>
          영상 보기
        </button>

        ${
          hasUrl
            ? `<a href="${escapeAttribute(cctv.url)}" target="_blank" rel="noopener noreferrer" class="btn btn-secondary btn-sm">새 탭 확인</a>`
            : ""
        }
      </div>
    `;

    const playButton = item.querySelector(".play-cctv-btn");

    if (playButton) {
      playButton.addEventListener("click", () => {
        playCctv(cctv);
      });
    }

    listBox.appendChild(item);
  });
}

function playCctv(cctv) {
  const video = getElement("traffic-video-player");
  const image = getElement("traffic-image-player");
  const placeholder = getElement("traffic-player-placeholder");
  const selectedName = getElement("selected-cctv-name");
  const selectedLink = getElement("selected-cctv-link");

  const url = cctv.url;

  console.log("[SELECTED CCTV]", cctv);
  console.log("[CCTV URL]", url);

  if (!url) {
    showError("선택한 CCTV에 영상 URL이 없습니다.");
    return;
  }

  showError("");

  selectedName.textContent = cctv.name || "선택한 CCTV";

  selectedLink.href = url;
  selectedLink.style.display = "inline-block";

  placeholder.style.display = "none";
  image.style.display = "none";
  image.removeAttribute("src");

  video.style.display = "none";

  stopPreviousPlayer(video);

  const lowerUrl = url.toLowerCase();

  if (
    lowerUrl.includes(".jpg") ||
    lowerUrl.includes(".jpeg") ||
    lowerUrl.includes(".png")
  ) {
    image.src = url;
    image.style.display = "block";
    return;
  }

  video.style.display = "block";

  if (lowerUrl.includes(".m3u8")) {
    playHls(video, url);
    return;
  }

  video.src = url;
  video.load();

  video.play().catch((error) => {
    console.error("[VIDEO PLAY ERROR]", error);
    showError("자동 재생이 차단되었거나 브라우저에서 바로 재생할 수 없는 URL입니다. 새 탭 확인을 눌러보세요.");
  });
}

function playHls(video, url) {
  if (video.canPlayType("application/vnd.apple.mpegurl")) {
    video.src = url;
    video.load();

    video.play().catch((error) => {
      console.error("[HLS NATIVE PLAY ERROR]", error);
      showError("HLS 자동 재생에 실패했습니다. 영상 재생 버튼을 눌러보세요.");
    });

    return;
  }

  if (window.Hls && window.Hls.isSupported()) {
    hlsInstance = new window.Hls({
      enableWorker: true
    });

    hlsInstance.loadSource(url);
    hlsInstance.attachMedia(video);

    hlsInstance.on(window.Hls.Events.MANIFEST_PARSED, () => {
      video.play().catch((error) => {
        console.error("[HLS PLAY ERROR]", error);
        showError("HLS 자동 재생에 실패했습니다. 영상 재생 버튼을 눌러보세요.");
      });
    });

    hlsInstance.on(window.Hls.Events.ERROR, (event, data) => {
      console.error("[HLS ERROR]", data);

      if (data && data.fatal) {
        showError("HLS 영상 재생 중 오류가 발생했습니다. 새 탭 확인 또는 다른 CCTV 유형을 선택해보세요.");
      }
    });

    return;
  }

  showError("현재 브라우저에서 HLS 영상을 재생할 수 없습니다.");
}

function stopPreviousPlayer(video) {
  if (hlsInstance) {
    hlsInstance.destroy();
    hlsInstance = null;
  }

  video.pause();
  video.removeAttribute("src");
  video.load();
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttribute(value) {
  return escapeHtml(value);
}

document.addEventListener("DOMContentLoaded", () => {
  const regionPreset = getElement("regionPreset");
  const loadButton = getElement("load-cctv-btn");

  if (regionPreset) {
    regionPreset.addEventListener("change", () => {
      applyRegionPreset(regionPreset.value);
    });
  }

  if (loadButton) {
    loadButton.addEventListener("click", loadCctvList);
  }

  applyRegionPreset("seoul");
});