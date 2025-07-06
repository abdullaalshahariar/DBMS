(async () => {
  const holder = document.getElementById('request-donation-short');
  if (!holder.dataset.loaded) {
    try {
      const response = await fetch('htmls/request-donation.html');
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      holder.innerHTML = await response.text();
      holder.dataset.loaded = 'true';
    } catch (err) {
      return;
    }
  }
})();
