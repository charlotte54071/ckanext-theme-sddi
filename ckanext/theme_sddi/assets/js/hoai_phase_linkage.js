// HOAI mapping for lifecycle phases
const hoaiPhaseMap = {
  'pre-construction': ['LPH 1', 'LPH 2', 'LPH 6', 'LPH 7'],
  'survey': ['LPH 1'],
  'design': ['LPH 3', 'LPH 4', 'LPH 5'],
  'construction': ['LPH 8'],
  'retirement': [] 
};

(function(){
  function findField(name) {
    return (
      document.querySelector('select[name="' + name + '"]') ||
      document.querySelector('input[name="' + name + '"]') ||
      document.querySelector('[id*="' + name + '"]')
    );
  }

  const lifecyclePhase = findField('lifecycle_phase');
  const hoaiPhase = findField('hoai_phase');

  if (!lifecyclePhase || !hoaiPhase) {
    console.warn('[hoai_phase_linkage.js] 字段未找到！', {
      lifecyclePhase, hoaiPhase
    });
    return;
  }

  function updateHoaiOptions(phaseKey) {
    const allowedPhases = hoaiPhaseMap[phaseKey] || [];
    
    // 清空当前 options
    hoaiPhase.innerHTML = '';

    if (allowedPhases.length === 0) {
      hoaiPhase.disabled = true;
      return;
    }

    // 添加允许的选项
    for (const phase of allowedPhases) {
      const option = document.createElement('option');
      option.value = phase;
      option.textContent = phase;
      hoaiPhase.appendChild(option);
    }

    hoaiPhase.disabled = false;
  }

  lifecyclePhase.addEventListener('change', function() {
    const selected = lifecyclePhase.value;
    updateHoaiOptions(selected);
  });

  // 初始触发一次
  lifecyclePhase.dispatchEvent(new Event('change'));
})();
