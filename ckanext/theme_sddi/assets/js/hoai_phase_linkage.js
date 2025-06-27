// HOAI mapping for lifecycle phases
// This script dynamically updates the options for the HOAI phase field based on the selected lifecycle phase
const hoaiPhaseMap = {
  'pre-construction': ['LPH 1', 'LPH 2', 'LPH 6', 'LPH 7'],
  'survey': ['LPH 1'],
  'design': ['LPH 3', 'LPH 4', 'LPH 5'],
  'construction': ['LPH 8'],
  'operation': ['LPH 9'],
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

  // if the current value is not in the allowed options, reset it
  const current = $('#field-hoai_phase').val();
  if (current && !allowed.includes(current)) {
    $('#field-hoai_phase').val('');
  }
}

$(document).ready(function () {
  // initialize the hoai_phase options based on the current lifecycle_phase
  // This assumes that the lifecycle_phase field is already populated
  const selected = $('#field-lifecycle_phase').val();
  updateHoaiPhaseOptions(selected);

  // if the lifecycle_phase changes, update the hoai_phase options
  // This assumes that the lifecycle_phase field is a select element
  $('#field-lifecycle_phase').on('change', function () {
    const selected = $(this).val();
    updateHoaiPhaseOptions(selected);
  });
});
