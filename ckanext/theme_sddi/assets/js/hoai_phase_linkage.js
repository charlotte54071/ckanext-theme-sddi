// HOAI mapping for lifecycle phases
const hoaiPhaseMap = {
  'pre-construction': ['LPH 1', 'LPH 2', 'LPH 6', 'LPH 7'],
  'survey': ['LPH 1'],
  'design': ['LPH 3', 'LPH 4', 'LPH 5'],
  'construction': ['LPH 8'],
  'retirement': [] 
};

function updateHoaiPhaseOptions(selectedPhase) {
  const allowed = hoaiPhaseMap[selectedPhase] || [];

  $('#field-hoai_phase option').each(function () {
    const val = $(this).val();
    if (!val) return;
    if (allowed.includes(val)) {
      $(this).show();
    } else {
      $(this).hide();
    }
  });

  const current = $('#field-hoai_phase').val();
  if (current && !allowed.includes(current)) {
    $('#field-hoai_phase').val('');
  }
}

// 尝试等 200ms 后初始化，确保字段已经加载
$(document).ready(function () {
  setTimeout(function () {
    const $lifecycle = $('#field-lifecycle_phase');
    const $hoai = $('#field-hoai_phase');

    if ($lifecycle.length === 0 || $hoai.length === 0) {
      console.warn('hoai_phase_linkage.js: 字段未找到');
      return;
    }

    updateHoaiPhaseOptions($lifecycle.val());

    $lifecycle.on('change', function () {
      updateHoaiPhaseOptions($(this).val());
    });
  }, 200);
});
