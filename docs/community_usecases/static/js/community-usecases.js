/* DOM contract: #community-search; .community-filters buttons with
 * data-community-filter; .community-card[data-community-type][data-community-search];
 * .community-group per Sphinx section; localized #community-results count template.
 * Markup stays fully readable without JavaScript. No external dependencies.
 */
(() => {
  "use strict";

  function initializeCommunityUseCases() {
    const search = document.getElementById("community-search");
    if (!search || search.dataset.communityInitialized === "true") return;
    search.dataset.communityInitialized = "true";

    const normalize = (text) => String(text || "").normalize("NFKC").toLowerCase();
    const cards = Array.from(document.querySelectorAll(".community-card")).map((element) => ({
      element,
      type: element.dataset.communityType,
      text: normalize(element.dataset.communitySearch || element.textContent),
    }));
    const buttons = Array.from(document.querySelectorAll(".community-filters [data-community-filter]"));
    const results = document.getElementById("community-results");
    const empty = document.getElementById("community-empty");
    const countTemplate = results ? results.dataset.countTemplate || "{shown} of {total} entries" : "";
    const initialButton = buttons.find((button) => button.getAttribute("aria-pressed") === "true");
    let activeFilter = initialButton ? initialButton.dataset.communityFilter : "all";

    const sectionElements = new Set();
    const groups = Array.from(document.querySelectorAll(".community-group")).map((element) => {
      let section = element.closest("section");
      // Include category parents so their headings disappear with all their cards.
      // Stop at the controls' section; never hide the page/root heading or controls.
      while (section && !section.contains(search)) {
        if (!section.querySelector("h1")) sectionElements.add(section);
        section = section.parentElement ? section.parentElement.closest("section") : null;
      }
      return { element, cards: Array.from(element.querySelectorAll(".community-card")) };
    });
    const sections = Array.from(sectionElements).map((element) => ({
      element,
      cards: Array.from(element.querySelectorAll(".community-card")),
    }));

    function update() {
      // Every whitespace-separated query term must occur; substring matching also
      // supports Chinese queries and partial project names without word-boundary assumptions.
      const terms = normalize(search.value).trim().split(/\s+/u).filter(Boolean);
      let shown = 0;

      cards.forEach((card) => {
        const matchesType = activeFilter === "all" || card.type === activeFilter;
        const visible = matchesType && terms.every((term) => card.text.includes(term));
        card.element.hidden = !visible;
        if (visible) shown += 1;
      });

      groups.forEach((group) => {
        const hidden = !group.cards.some((card) => !card.hidden);
        group.element.hidden = hidden;
      });
      sections.forEach((section) => {
        section.element.hidden = !section.cards.some((card) => !card.hidden);
      });

      buttons.forEach((button) => {
        button.setAttribute("aria-pressed", String(button.dataset.communityFilter === activeFilter));
      });

      if (results) {
        results.textContent = countTemplate
          .replace(/\{shown\}/g, String(shown))
          .replace(/\{total\}/g, String(cards.length));
      }
      if (empty) empty.hidden = shown !== 0;
    }

    search.addEventListener("input", update);
    search.addEventListener("search", update);
    buttons.forEach((button) => {
      button.addEventListener("click", (event) => {
        event.preventDefault();
        activeFilter = button.dataset.communityFilter;
        update();
      });
    });
    document.querySelectorAll(".community-highlight, .community-jump a").forEach((link) => {
      link.addEventListener("click", () => {
        // A linked case or section may be hidden by the current search or filter.
        search.value = "";
        activeFilter = "all";
        update();
      });
    });
    update();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeCommunityUseCases, { once: true });
  } else {
    initializeCommunityUseCases();
  }
})();
