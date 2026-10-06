"use strict";
const {config, notes} = window.PAPERLIST;
const $ = id => document.getElementById(id);
const el = (tag, cls, text) => {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text !== undefined) node.textContent = text;
  return node;
};
function link(text, url, cls) {
  const a = el("a", cls, text); a.href = url; a.target = "_blank"; a.rel = "noopener noreferrer"; return a;
}
function localDate(value) {
  const parts = new Intl.DateTimeFormat("en-US", {timeZone:config.timezone, year:"numeric", month:"2-digit", day:"2-digit"}).formatToParts(new Date(value));
  const read = type => Number(parts.find(p => p.type === type).value);
  return new Date(Date.UTC(read("year"), read("month") - 1, read("day")));
}
function isoWeek(date) {
  const d = new Date(date); d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7));
  const year = d.getUTCFullYear();
  const week = Math.ceil((((d - Date.UTC(year,0,1)) / 86400000) + 1) / 7);
  return `${year}-W${String(week).padStart(2,"0")}`;
}
function weekLabel(week) {
  const [year, number] = week.split("-W").map(Number);
  const jan4 = new Date(Date.UTC(year, 0, 4));
  jan4.setUTCDate(jan4.getUTCDate() - (jan4.getUTCDay() || 7) + 1 + (number - 1) * 7);
  const end = new Date(jan4); end.setUTCDate(end.getUTCDate() + 6);
  const format = d => d.toLocaleDateString("en-US", {month:"short",day:"numeric", timeZone:"UTC"});
  return `${format(jan4)} – ${format(end)}, ${end.getUTCFullYear()}`;
}
const dateLabel = value => new Date(value).toLocaleDateString("en-US", {month:"short",day:"numeric",year:"numeric",timeZone:config.timezone});
let view = "week";
$("site-title").textContent = config.title;
document.title = `${config.title} · UIUC-MLSys`;
$("subtitle").textContent = config.subtitle;
$("repo-link").href = config.repository;
$("contribute-link").href = `${config.repository}/blob/main/CONTRIBUTING.md`;
$("guide-link").href = $("contribute-link").href;
$("timezone-note").textContent = `Weeks run Monday–Sunday in ${config.timezone}. Aim for ${config.weekly_target} papers per week.`;
$("examples").checked = !notes.some(n => !n.example);
const library = () => notes.filter(n => n.example === $("examples").checked);
function options(id, items) {
  const value = $(id).value;
  while ($(id).options.length > 1) $(id).remove(1);
  for (const [key, label] of items) { const option = el("option", "", label); option.value = key; $(id).append(option); }
  $(id).value = items.some(([key]) => key === value) ? value : "";
}
function refreshFilters() {
  const active = library();
  options("topic", Object.entries(config.topics));
  options("week", [...new Set(active.map(n => n.week))].sort().reverse().map(w => [w, w]));
  const members = $("examples").checked ? Object.fromEntries(active.map(n => [n.member, n.member_name])) : config.members;
  options("member", Object.entries(members));
}
function tags(topics) {
  const wrap = el("div", "tags");
  for (const t of topics) {
    const b = el("button", "tag", config.topics[t]);
    b.addEventListener("click", () => { $("topic").value = t; render(); }); wrap.append(b);
  }
  return wrap;
}
function paperTable(papers, name) {
  const wrap = el("div", "table-scroll"); wrap.tabIndex = 0;
  wrap.setAttribute("role", "region"); wrap.setAttribute("aria-label", `${name} papers`);
  const table = el("table", "paper-table"), head = el("thead"), header = el("tr"), body = el("tbody");
  const caption = el("caption", "sr-only", name); table.append(caption);
  for (const label of ["Paper", "Year / venue", "Topics", "Added by", "Added"] ) {
    const th = el("th", "", label); th.scope = "col"; header.append(th);
  }
  head.append(header); table.append(head, body);
  const rows = [...papers.values()];
  const mode = $("sort").value;
  rows.sort((a, b) => {
    const x = a[0], y = b[0];
    if (mode === "title") return x.title.localeCompare(y.title);
    if (mode === "year") return y.year - x.year || x.title.localeCompare(y.title);
    const order = new Date(y.added_at) - new Date(x.added_at);
    return (mode === "oldest" ? -order : order) || x.title.localeCompare(y.title);
  });
  for (const entries of rows) {
    const n = entries[0], row = el("tr"), paper = el("td", "paper-cell");
    paper.append(link(n.title, n.url, "paper-title-link"));
    if (n.code_url) paper.append(document.createTextNode(" "), link("Code ↗", n.code_url, "paper-link"));
    const publication = el("td", "publication");
    publication.append(el("span", "", n.year), el("small", "", n.venue || ""));
    const topicCell = el("td"); topicCell.append(tags([...new Set(entries.flatMap(e => e.topics))]));
    const members = el("td", "contributors");
    for (const entry of entries) {
      const source = link(entry.member_name, `${config.repository}/blob/main/${entry.source}`, "source-link");
      source.title = `Source: ${entry.source}`; members.append(source);
    }
    const dates = el("td", "added-dates");
    for (const entry of entries) {
      const date = el("span", "", dateLabel(entry.added_at));
      date.title = `${entry.member_name} · ${entry.week}${entry.pending ? " · Preview date" : ""}`;
      dates.append(date);
    }
    row.append(paper, publication, topicCell, members, dates); body.append(row);
  }
  wrap.append(table); return wrap;
}
function memberStats(member, all) {
  const today = localDate(new Date()), current = isoWeek(today);
  const recent = new Set(Array.from({length:4}, (_, i) => isoWeek(new Date(today.getTime() - i * 7 * 86400000))));
  const entries = all.filter(n => n.member === member);
  const strip = el("div", "member-stats");
  for (const [value, label] of [[entries.filter(n => n.week === current).length, "this week"], [(entries.filter(n => recent.has(n.week)).length / 4).toFixed(1), "per week · last 4 weeks"], [config.weekly_target, "weekly goal"]]) {
    const item = el("span"); item.append(el("strong", "", value), el("small", "", label)); strip.append(item);
  }
  return strip;
}
function render() {
  const all = library(), query = $("search").value.trim().toLowerCase();
  const current = isoWeek(localDate(new Date()));
  $("example-banner").hidden = !$("examples").checked;
  $("stats").replaceChildren();
  for (const [value, label] of [[new Set(all.map(n => n.paper_id)).size, "PAPERS IN THE LIBRARY"], [all.filter(n => n.week === current).length, "SUBMISSIONS THIS WEEK"], [new Set(all.flatMap(n => n.topics)).size, "RESEARCH TOPICS"], [$("examples").checked ? new Set(all.map(n => n.member)).size : Object.keys(config.members).length, "READERS"]]) {
    const stat = el("div", "stat"); stat.append(el("strong", "", value), el("span", "", label)); $("stats").append(stat);
  }
  const filtered = all.filter(n => (!$("topic").value || n.topics.includes($("topic").value)) && (!$("week").value || n.week === $("week").value) && (!$("member").value || n.member === $("member").value) && (!query || `${n.title} ${n.paper_id} ${n.member_name} ${n.venue || ""}`.toLowerCase().includes(query)));
  const titles = {week:["THE WEEKLY EDIT", "A little reading, every week."], topic:["FOLLOW A THREAD", "Ideas across research areas."], member:["THE PEOPLE BEHIND THE PAPERS", "A shared reading habit."]};
  $("view-kicker").textContent = titles[view][0]; $("view-title").textContent = titles[view][1];
  const paperCount = new Set(filtered.map(n => n.paper_id)).size;
  $("result-count").textContent = `${paperCount} ${paperCount === 1 ? "paper" : "papers"} · ${filtered.length} ${filtered.length === 1 ? "submission" : "submissions"}${$("examples").checked ? " · example data" : ""}`;
  document.querySelectorAll("[data-view]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.view === view)));
  const groups = new Map();
  for (const n of filtered) {
    const keys = view === "week" ? [n.week] : view === "member" ? [n.member] : n.topics.filter(t => !$("topic").value || t === $("topic").value);
    for (const key of keys) { if (!groups.has(key)) groups.set(key, []); groups.get(key).push(n); }
  }
  if (view === "member" && !query && !$("topic").value && !$("week").value && !$("examples").checked) {
    for (const member of Object.keys(config.members)) if ((!$("member").value || $("member").value === member) && !groups.has(member)) groups.set(member, []);
  }
  $("results").replaceChildren();
  for (const key of [...groups.keys()].sort((a,b) => view === "week" ? b.localeCompare(a) : a.localeCompare(b))) {
    const entries = groups.get(key), section = el("section", "group"), header = el("div", "group-heading");
    const name = view === "week" ? weekLabel(key) : view === "topic" ? config.topics[key] : (config.members[key] || "Example reader");
    header.append(el("h3", "", name), el("span", "", `${view === "week" ? key + " · " : ""}${entries.length} ${entries.length === 1 ? "submission" : "submissions"}`)); section.append(header);
    if (view === "member") section.append(memberStats(key, all));
    const papers = new Map();
    for (const note of entries) { if (!papers.has(note.paper_id)) papers.set(note.paper_id, []); papers.get(note.paper_id).push(note); }
    if (papers.size) section.append(paperTable(papers, name));
    if (!entries.length) section.append(el("p", "note-caption", "No papers submitted yet. Start with the weekly YAML template."));
    $("results").append(section);
  }
  if (!groups.size) {
    const empty = el("div", "empty");
    empty.append(el("h3", "", all.length ? "No papers match these filters." : "Your reading library starts here."), el("p", "", all.length ? "Try another keyword or reset the filters." : "Fill in the weekly YAML template and push it to the repository."));
    if (!all.length) empty.append(link("Open the contribution guide ↗", $("guide-link").href, "paper-link")); $("results").append(empty);
  }
}
document.querySelectorAll("[data-view]").forEach(b => b.addEventListener("click", () => {view = b.dataset.view; render();}));
for (const id of ["search", "topic", "week", "member", "sort"]) $(id).addEventListener(id === "search" ? "input" : "change", render);
$("examples").addEventListener("change", () => {refreshFilters(); render();});
$("clear").addEventListener("click", () => { for (const id of ["search", "topic", "week", "member"]) $(id).value = ""; $("sort").value = "newest"; render(); });
refreshFilters(); render();
