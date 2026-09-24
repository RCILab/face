# 추가 영상 재료 교체 목록

컵·달걀·케첩 닦기 실험은 최종 영상에서 추출한 개별 클립으로 재생됩니다. 케첩 닦기는 논문 외 추가 실험의 예시로 소개합니다.

| 위치 | 가져올 재료 | 권장 파일명 | 현재 연결 |
| --- | --- | --- | --- |
| Paper cups | 원본 클립으로 교체 가능 | `static/videos/cup-comparison.mp4` | 반영 완료: 00:47–00:58.2 + 마지막 프레임 1초 유지 |
| Eggs | 원본 클립으로 교체 가능 | `static/videos/egg-comparison.mp4` | 반영 완료: 01:21.5–01:37.2 + 마지막 프레임 1초 유지 |
| Ketchup wiping | 원본 클립으로 교체 가능 | `static/videos/ketchup-wiping.mp4` | 반영 완료: FACE 구간 02:25–02:35.6 + 마지막 프레임 1초 유지 |
| Hardware (선택) | handheld demonstration 원본 | `static/videos/handheld-demo.mp4` | 논문 Figure 3 |
| Method (선택) | encoder / decoder / contact estimation 애니메이션 원본 | `static/videos/method.mp4` | 논문 Figure 2 |

## 교체 방법

원본을 받으면 위 경로의 MP4를 교체하면 됩니다. 세 실험 모두 다음과 같은 네이티브 video 요소를 사용합니다.

```html
<video controls playsinline preload="metadata" poster="static/images/geometry.jpg"
       aria-label="Cup marking comparison">
  <source src="static/videos/cup-comparison.mp4" type="video/mp4">
</video>
```

세 실험 영상은 무음 자동 반복 재생되며 기본 영상 컨트롤로 일시정지·탐색할 수 있습니다. 추출 구간은 `scripts/prepare_assets.py`에 기록되어 있습니다. 케첩 닦기 클립은 Full Method 구간만 사용하며, 원본에 포함된 결과 표시와 재생 속도 표기를 유지합니다.

## 원본과 출처

- 논문: `_2026__ICRA___FACE (2).pdf` → `static/pdfs/face-paper.pdf` (원본 그대로)
- 최종 영상: `ICRA27_3998_VI_i-2.mp4` → `static/videos/face-final.mp4` (재인코딩 없이 MP4 faststart 처리)
- 상단 미리보기: 최종 영상 00:48–00:58.2, 여섯 Success 표시가 모두 나온 마지막 프레임을 1초 고정한 후 반복하는 음소거 루프
- 각 이미지: `scripts/prepare_assets.py`에 원본 페이지·크롭 좌표·영상 시각 기록
- 수치: 논문 Table I / II. 컵 변형 20회, 표면 변화 30회, 달걀 25회에 대해 nominal 조건을 제외하여 집계
- 익명 저자 표기를 유지했으며, 저자 이름·게재 확정·코드 공개 일정은 추가하지 않았습니다.

본문은 영어이며, 이 파일은 초안 편집을 위한 한국어 메모입니다.
