// HOAI mapping for lifecycle phases
const hoaiPhaseMap = {
  'pre-construction': ['LPH 1', 'LPH 2', 'LPH 6', 'LPH 7'],
  'survey': ['LPH 1'],
  'design': ['LPH 3', 'LPH 4', 'LPH 5'],
  'construction': ['LPH 8'],
  'retirement': [] 
};

// hoai_phase_linkage.js
(function(){
  // 尝试多种方式查找表单控件
  function findField(name) {
    return (
      document.querySelector('select[name="' + name + '"]') ||
      document.querySelector('input[name="' + name + '"]') ||
      document.querySelector('[id*="' + name + '"]')
    );
  }

  // 找到控件
  const lifecyclePhase = findField('lifecycle_phase');
  const hoaiPhase = findField('hoai_phase');

  if (!lifecyclePhase || !hoaiPhase) {
    console.warn('[hoai_phase_linkage.js] 字段未找到！', {
      lifecyclePhase, hoaiPhase
    });
    return;
  }

  // 举例：lifecycle_phase 变化时，更新 hoai_phase 选项
  lifecyclePhase.addEventListener('change', function() {
    // 可以根据 lifecyclePhase.value 动态改变 hoaiPhase 的选项、可用性等
    // 举例：如果生命周期选某个值，只允许 hoai_phase 选第一个选项
    if (lifecyclePhase.value === '只允许第一个') {
      hoaiPhase.value = hoaiPhase.options[0]?.value || '';
      hoaiPhase.disabled = true;
    } else {
      hoaiPhase.disabled = false;
    }
  });

  // 可根据需要添加更多联动逻辑

  // 初始触发一次，保证状态同步
  lifecyclePhase.dispatchEvent(new Event('change'));
})();
