const userSelect = document.querySelector('#user-select');
const limitSelect = document.querySelector('#limit-select');
const refreshButton = document.querySelector('#refresh-button');
const feed = document.querySelector('#feed');
const empty = document.querySelector('#empty');
const errorBox = document.querySelector('#error');
const strategy = document.querySelector('#strategy');
const strategyText = document.querySelector('#strategy-text');
const healthLabel = document.querySelector('#health-label');
const statusDot = document.querySelector('.status-dot');
const cardTemplate = document.querySelector('#card-template');

const titleFrom = (post, fallback) => post.title || post.caption || `A handpicked discovery #${fallback}`;
const descriptionFrom = post => post.description || post.caption || 'A fresh recommendation selected for your personal commerce feed.';
const categoryFrom = post => post.category || post.category_id || 'For you';
const humanize = value => String(value).replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());

function setView(view) {
  feed.hidden = view !== 'feed'; empty.hidden = view !== 'empty'; errorBox.hidden = view !== 'error';
}

function renderRecommendations(items) {
  feed.innerHTML = '';
  if (!items.length) { setView('empty'); return; }
  const fragment = document.createDocumentFragment();
  items.forEach((item, index) => {
    const node = cardTemplate.content.cloneNode(true);
    const post = item.post || {};
    node.querySelector('.art-index').textContent = String(index + 1).padStart(2, '0');
    node.querySelector('.category').textContent = categoryFrom(post);
    node.querySelector('.score').textContent = `${Math.round((item.score || 0) * 100)}% match`;
    node.querySelector('.post-title').textContent = titleFrom(post, index + 1);
    node.querySelector('.post-description').textContent = descriptionFrom(post);
    const reasons = node.querySelector('.reason-list');
    (item.reason || []).slice(0, 2).forEach(reason => { const tag = document.createElement('span'); tag.className = 'reason'; tag.textContent = reason; reasons.append(tag); });
    const breakdown = node.querySelector('.breakdown');
    Object.entries(item.score_breakdown || {}).forEach(([key, value]) => {
      const row = document.createElement('div'); row.innerHTML = `<span>${humanize(key)}</span><b>${Math.round(value * 100)}%</b>`; breakdown.append(row);
    });
    fragment.append(node);
  });
  feed.append(fragment); setView('feed');
}

async function loadFeed() {
  const userId = userSelect.value;
  if (!userId) { setView('empty'); return; }
  refreshButton.disabled = true; refreshButton.innerHTML = '<span>↻</span> Building feed';
  try {
    const response = await fetch(`/recommend/${encodeURIComponent(userId)}?limit=${limitSelect.value}`);
    if (!response.ok) throw new Error('The recommendation service is unavailable.');
    const data = await response.json();
    strategyText.textContent = humanize(data.strategy || 'personalized'); strategy.hidden = false;
    renderRecommendations(data.recommendations || []);
  } catch (err) { document.querySelector('#error-message').textContent = err.message; setView('error'); }
  finally { refreshButton.disabled = false; refreshButton.innerHTML = '<span>↻</span> Refresh feed'; }
}

async function initialize() {
  try {
    const response = await fetch('/health'); const health = await response.json();
    const online = health.status === 'healthy'; healthLabel.textContent = online ? 'Recommendation engine online' : 'Database reconnecting';
    statusDot.classList.toggle('online', online);
  } catch { healthLabel.textContent = 'Service status unavailable'; }
  try {
    const response = await fetch('/users/sample');
    if (!response.ok) throw new Error();
    const { user_ids: users = [] } = await response.json();
    userSelect.innerHTML = '';
    if (!users.length) throw new Error();
    users.forEach((id, index) => { const option = new Option(`User ${id}`, id, index === 0, index === 0); userSelect.add(option); });
    await loadFeed();
  } catch {
    userSelect.innerHTML = '<option value="">No sample users available</option>';
    setView('empty');
  }
}
refreshButton.addEventListener('click', loadFeed);
userSelect.addEventListener('change', loadFeed);
limitSelect.addEventListener('change', loadFeed);
initialize();
