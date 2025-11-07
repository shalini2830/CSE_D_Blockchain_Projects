document.addEventListener('DOMContentLoaded', () => {
  // Preserve form state for forms marked with data-preserve
  const forms = document.querySelectorAll('form[data-preserve="true"]');
  forms.forEach((form, idx) => {
    const key = location.pathname + '#' + (form.id || idx);
    // restore
    const saved = sessionStorage.getItem(key);
    if (saved) {
      try {
        const data = JSON.parse(saved);
        Object.keys(data).forEach(name => {
          const el = form.querySelector(`[name="${name}"]`);
          if (el) el.value = data[name];
        });
      } catch {}
    }
    // save on input
    form.addEventListener('input', () => {
      const data = {};
      Array.from(form.elements).forEach(el => {
        if (el.name) data[el.name] = el.value;
      });
      sessionStorage.setItem(key, JSON.stringify(data));
    });
  });
});


