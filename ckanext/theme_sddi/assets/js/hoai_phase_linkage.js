// assets/js/hoai_phase_linkage.js
require(['jquery'], function($) {
  $(function() {
    const $lc = $('#field-lifecycle_phase');
    const $hp = $('#field-hoai_phase');
    if (!$lc.length || !$hp.length) {
      return;  // 只有在资源表单里这两个字段都存在时才继续
    }

    const hoaiPhaseMap = {
      'pre-construction': ['LPH 1','LPH 2','LPH 6','LPH 7'],
      'survey':           ['LPH 1'],
      'design':           ['LPH 3','LPH 4','LPH 5'],
      'construction':     ['LPH 8'],
      'operation':        ['LPH 9'],
      'retirement':       []
    };

    function update() {
      const sel = $lc.val() || '';
      const allow = hoaiPhaseMap[sel] || [];
      $hp.find('option').each(function() {
        const v = this.value;
        if (!v) return;
        $(this).toggle(allow.includes(v));
      });
      if ($hp.val() && !allow.includes($hp.val())) {
        $hp.val('');
      }
    }

    // 初始化 & 绑定事件
    update();
    $lc.on('change', update);
  });
});
