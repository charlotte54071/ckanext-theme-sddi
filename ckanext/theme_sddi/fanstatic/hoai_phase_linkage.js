this.ckan.module('hoai_phase_linkage', function ($, _) {
  return {
    initialize: function () {
      const $lc = $('[name="lifecycle_phase"]');
      const $hp = $('[name="hoai_phase"]');

      const hoaiPhaseMap = {
        'pre-construction': ['LPH 1','LPH 2','LPH 6','LPH 7'],
        'survey':           ['LPH 1'],
        'design':           ['LPH 3','LPH 4','LPH 5'],
        'construction':     ['LPH 8'],
        'operation':        ['LPH 9'],
        'retirement':       []
      };

      const update = () => {
        const sel = $lc.val() || '';
        const allow = hoaiPhaseMap[sel] || [];

        $hp.find('option').each(function () {
          const v = this.value;
          if (!v) return;
          $(this).toggle(allow.includes(v));
        });

        if ($hp.val() && !allow.includes($hp.val())) {
          $hp.val('');
        }
      };

      update();
      $lc.on('change', update);
    }
  };
});
