"use client";

import { useState, useCallback, useRef, useEffect, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";

const ease = [0.22, 1, 0.36, 1] as const;

export type SectionCategory = "all" | "switch" | "core" | "plans" | "dsa" | "prep" | "cheats";

export interface RoadmapSection {
  id: string;
  title: string;
  cat: "core" | "plans" | "dsa" | "prep" | "switch" | "cheats";
  icon?: string;
}

export const ALL_SECTIONS: RoadmapSection[] = [
  { id: "s1", title: "Reality Check", cat: "core", icon: "💡" },
  { id: "s2", title: "Phase 1: Foundations", cat: "core", icon: "📐" },
  { id: "s3", title: "Phase 2: ML & Deep Learning", cat: "core", icon: "🧠" },
  { id: "s4", title: "Phase 3: GenAI & LLMs", cat: "core", icon: "⚡" },
  { id: "s5", title: "Phase 4: AI Infrastructure", cat: "core", icon: "🏗️" },
  { id: "s15", title: "OS & C++ Deep Dive", cat: "core", icon: "⚙️" },
  { id: "s18", title: "Research Papers", cat: "core", icon: "📑" },
  { id: "s11", title: "Phase 1 Day Plan", cat: "plans", icon: "📅" },
  { id: "s12", title: "Phase 2 Day Plan", cat: "plans", icon: "📅" },
  { id: "s13", title: "Phase 3 Day Plan", cat: "plans", icon: "📅" },
  { id: "s14", title: "Phase 4 Day Plan", cat: "plans", icon: "📅" },
  { id: "s6", title: "DSA Cockpit (168D) ↗", cat: "dsa", icon: "🚀" },
  { id: "s7", title: "System Design", cat: "dsa", icon: "🌐" },
  { id: "s8", title: "Projects Portfolio", cat: "prep", icon: "🛠️" },
  { id: "s9", title: "Interviews & Prep", cat: "prep", icon: "🎯" },
  { id: "s10", title: "Brutal Advice", cat: "prep", icon: "🔥" },
  { id: "s16", title: "Sustainability", cat: "prep", icon: "🌿" },
  { id: "s17", title: "Strategy & Execution", cat: "prep", icon: "🧭" },
  { id: "s25", title: "Career Switch (Roadmap.sh)", cat: "switch", icon: "🚀" },
  { id: "s21", title: "Python Cheat Sheet", cat: "cheats", icon: "🐍" },
  { id: "s22", title: "Git Cheat Sheet", cat: "cheats", icon: "🌿" },
  { id: "s24", title: "C++ Cheat Sheet", cat: "cheats", icon: "⚙️" },
  { id: "s26", title: "Master Timetable", cat: "cheats", icon: "⏱️" },
  { id: "s27", title: "Weekly Log", cat: "cheats", icon: "📓" },
];

export interface FloatingMenuProps {
  sections?: RoadmapSection[];
  onSelectSection?: (id: string) => void;
  activeId?: string;
}

// Kinetic character roll on hover
function KineticCharRoll({ text, hovered }: { text: string; hovered: boolean }) {
  const chars = text.split("");
  return (
    <span className="inline-flex items-center overflow-hidden h-[1.25em] leading-[1.25em]">
      {chars.map((char, i) => (
        <span key={i} className="inline-block overflow-hidden" style={{ height: "1.25em" }}>
          <span
            className="flex flex-col"
            style={{
              transitionProperty: "transform",
              transitionDuration: hovered ? "600ms" : "0ms",
              transitionDelay: hovered ? `${Math.min(i * 18, 360)}ms` : "0ms",
              transform: hovered ? "translateY(-50%)" : "translateY(0%)",
              transitionTimingFunction: "cubic-bezier(0.22, 1, 0.36, 1)",
            }}
          >
            <span className="block h-[1.25em] leading-[1.25em]">
              {char === " " ? "\u00A0" : char}
            </span>
            <span className="block h-[1.25em] leading-[1.25em] text-[#FFE862] font-extrabold" aria-hidden>
              {char === " " ? "\u00A0" : char}
            </span>
          </span>
        </span>
      ))}
    </span>
  );
}

export default function FloatingMenu({
  sections = ALL_SECTIONS,
  onSelectSection,
  activeId: initialActiveId,
}: FloatingMenuProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [isAutoHidden, setIsAutoHidden] = useState(false);
  const [activeCategory, setActiveCategory] = useState<SectionCategory>("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [activeId, setActiveId] = useState(initialActiveId || "s1");
  const [isDarkTheme, setIsDarkTheme] = useState(false);

  const containerRef = useRef<HTMLDivElement>(null);
  const searchInputRef = useRef<HTMLInputElement>(null);
  const lastScrollY = useRef(0);

  // Sync active ID from DOM
  useEffect(() => {
    const checkActive = () => {
      const activeEl = document.querySelector(".page.active");
      if (activeEl && activeEl.id) {
        setActiveId(activeEl.id);
      }
      const isDark = document.documentElement.getAttribute("data-theme") === "dark";
      setIsDarkTheme(isDark);
    };

    checkActive();
    const observer = new MutationObserver(checkActive);
    observer.observe(document.body, { attributes: true, subtree: true, attributeFilter: ["class"] });
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });

    return () => observer.disconnect();
  }, []);

  // Smart Auto-Hide on Scroll Down & Reveal on Scroll Up
  useEffect(() => {
    const handleScroll = () => {
      const currentY = window.scrollY;
      const delta = currentY - lastScrollY.current;

      // Only auto-hide when scrolled down significantly and menu is not open
      if (!isOpen) {
        if (currentY > 120 && delta > 8) {
          // Scrolling down -> hide
          setIsAutoHidden(true);
        } else if (delta < -8 || currentY <= 80) {
          // Scrolling up or at top -> reveal
          setIsAutoHidden(false);
        }
      }

      lastScrollY.current = currentY;
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, [isOpen]);

  // Reveal when mouse hovers near bottom of screen
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (isAutoHidden && e.clientY >= window.innerHeight - 48) {
        setIsAutoHidden(false);
      }
    };
    window.addEventListener("mousemove", handleMouseMove, { passive: true });
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, [isAutoHidden]);

  // Keyboard shortcut: Press M to toggle, Escape to close
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement;
      const isInput =
        target.tagName === "INPUT" ||
        target.tagName === "TEXTAREA" ||
        target.isContentEditable;

      if (e.key === "Escape" && isOpen) {
        setIsOpen(false);
      } else if ((e.key === "m" || e.key === "M") && !isInput && !e.metaKey && !e.ctrlKey) {
        e.preventDefault();
        setIsAutoHidden(false);
        setIsOpen((prev) => !prev);
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen]);

  // Focus search input when menu opens
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => {
        searchInputRef.current?.focus();
      }, 300);
    } else {
      setSearchQuery("");
    }
  }, [isOpen]);

  // Close on outside click
  useEffect(() => {
    if (!isOpen) return;
    const handler = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [isOpen]);

  // Filter sections by category and search query
  const filteredSections = useMemo(() => {
    let list = sections;
    if (activeCategory !== "all") {
      list = list.filter((s) => s.cat === activeCategory);
    }
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase().trim();
      list = list.filter(
        (s) =>
          s.title.toLowerCase().includes(q) ||
          s.id.toLowerCase().includes(q) ||
          s.cat.toLowerCase().includes(q)
      );
    }
    return list;
  }, [sections, activeCategory, searchQuery]);

  // Handle section selection
  const handleSelect = useCallback(
    (id: string) => {
      setActiveId(id);
      if (onSelectSection) {
        onSelectSection(id);
      } else if (window.show) {
        window.show(id);
      }
      setIsOpen(false);
    },
    [onSelectSection]
  );

  const activeSectionMeta = sections.find((s) => s.id === activeId);

  const categoryCounts = useMemo(() => {
    const counts: Record<string, number> = { all: sections.length };
    sections.forEach((s) => {
      counts[s.cat] = (counts[s.cat] || 0) + 1;
    });
    return counts;
  }, [sections]);

  return (
    <>
      {/* Subtle summon dock trigger when button is auto-hidden */}
      <AnimatePresence>
        {isAutoHidden && !isOpen && (
          <motion.button
            key="summon-dock"
            initial={{ opacity: 0, y: 30, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 30, scale: 0.9 }}
            transition={{ duration: 0.3, ease }}
            onClick={() => {
              setIsAutoHidden(false);
              setIsOpen(true);
            }}
            title="Click or press M to summon roadmap menu"
            className="fixed bottom-4 left-1/2 -translate-x-1/2 z-[9998] flex items-center gap-2.5 px-4 py-2 rounded-full bg-[#18181b]/90 text-[#f7f1ed] text-xs font-bold shadow-2xl border border-white/15 backdrop-blur-md hover:bg-[#FFE862] hover:text-[#18181b] hover:border-[#FFE862] transition-all duration-200 cursor-pointer group"
          >
            <span className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399] animate-pulse" />
            <span>✦ Roadmap Menu</span>
            <kbd className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-white/10 group-hover:bg-black/10 border border-white/20 group-hover:border-black/20">
              M
            </kbd>
          </motion.button>
        )}
      </AnimatePresence>

      {/* Main Liquid Morph Floating Menu Container */}
      <motion.div
        ref={containerRef}
        className="fixed bottom-6 left-1/2 z-[9999]"
        style={{ x: "-50%", pointerEvents: "auto" }}
        initial={{ opacity: 0, y: 20 }}
        animate={{
          opacity: isAutoHidden && !isOpen ? 0 : 1,
          y: isAutoHidden && !isOpen ? 90 : 0,
          pointerEvents: isAutoHidden && !isOpen ? "none" : "auto",
        }}
        transition={{ duration: 0.4, ease }}
      >
        <motion.div
          className="relative overflow-hidden flex flex-col shadow-[0_24px_60px_-10px_rgba(0,0,0,0.55),0_0_0_1px_rgba(255,255,255,0.08)]"
          onClick={() => {
            if (!isOpen) setIsOpen(true);
          }}
          style={{
            fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            cursor: isOpen ? "default" : "pointer",
          }}
          animate={{
            width: isOpen ? 680 : 164,
            height: isOpen ? 580 : 48,
            borderRadius: isOpen ? 24 : 72,
            scale: 1,
          }}
          whileHover={isOpen ? undefined : { scale: 1.04 }}
          transition={{
            duration: 0.65,
            ease,
            height: { duration: isOpen ? 0.6 : 0.25 },
            scale: { duration: 0.2, ease },
          }}
        >
          {/* Signature Yellow Outer Border & Glow Layer */}
          <motion.div
            className="absolute inset-0"
            animate={{
              backgroundColor: isOpen ? "#16161a" : "#FFE862",
              borderColor: isOpen ? "rgba(255, 232, 98, 0.4)" : "#d1bb3b",
            }}
            transition={{ duration: isOpen ? 0.2 : 0.35, ease }}
            style={{
              borderWidth: 1.5,
              borderStyle: "solid",
              borderRadius: "inherit",
            }}
          />

          {/* Dark circle expanding from bottom */}
          <motion.div
            className="absolute left-1/2 bg-[#16161a]"
            style={{
              width: "280%",
              height: "280%",
              borderRadius: "50%",
              x: "-50%",
            }}
            animate={{ bottom: isOpen ? "-20%" : "-280%" }}
            transition={{
              duration: 0.75,
              ease,
              delay: isOpen ? 0.05 : 0,
            }}
          />

          {/* EXPANDED MENU CONTENT (27 Sections, Search, Category Tabs) */}
          <div
            className="relative z-10 flex flex-col w-full h-full p-4 overflow-hidden"
            style={{
              pointerEvents: isOpen ? "auto" : "none",
              opacity: isOpen ? 1 : 0,
              display: isOpen ? "flex" : "none",
            }}
          >
            {/* Top Header Bar */}
            <div className="flex items-center justify-between gap-3 pb-3 border-b border-white/10 shrink-0">
              <div className="flex items-center gap-2.5 overflow-hidden">
                <span className="text-xs font-black tracking-wider uppercase bg-gradient-to-r from-[#FFE862] to-[#2dd4bf] bg-clip-text text-transparent whitespace-nowrap">
                  AI INFRA ROADMAP
                </span>
                {activeSectionMeta && (
                  <span className="hidden sm:inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-white/5 border border-white/10 text-[11px] text-[#f7f1ed] font-medium truncate max-w-[200px]">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 shrink-0" />
                    {activeSectionMeta.title}
                  </span>
                )}
              </div>

              {/* Quick Actions (Spotlight Search + Theme Toggle) */}
              <div className="flex items-center gap-1.5 shrink-0">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    window.openSearchModal?.();
                    setIsOpen(false);
                  }}
                  className="px-2.5 py-1 rounded-lg bg-white/5 hover:bg-white/15 border border-white/10 text-[11px] font-semibold text-[#f7f1ed] flex items-center gap-1.5 transition-all cursor-pointer"
                  title="Spotlight Search (Ctrl+K)"
                >
                  <span>🔍</span>
                  <kbd className="text-[9px] font-mono opacity-60">⌘K</kbd>
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    window.toggleDarkMode?.();
                    setIsDarkTheme((prev) => !prev);
                  }}
                  className="px-2.5 py-1 rounded-lg bg-white/5 hover:bg-white/15 border border-white/10 text-[11px] font-semibold text-[#f7f1ed] flex items-center gap-1 transition-all cursor-pointer"
                  title="Toggle Light / Dark Mode"
                >
                  <span>{isDarkTheme ? "☀️" : "🌙"}</span>
                </button>
              </div>
            </div>

            {/* Category Filter Rail */}
            <div className="flex items-center gap-1.5 py-2.5 overflow-x-auto no-scrollbar shrink-0 border-b border-white/5">
              {[
                { key: "all", label: `All (${categoryCounts.all || 27})` },
                { key: "switch", label: `🚀 Switch (${categoryCounts.switch || 1})` },
                { key: "core", label: `🏛️ Core (${categoryCounts.core || 7})` },
                { key: "plans", label: `📅 Plans (${categoryCounts.plans || 4})` },
                { key: "dsa", label: `💻 DSA (${categoryCounts.dsa || 4})` },
                { key: "prep", label: `🎯 Prep (${categoryCounts.prep || 5})` },
                { key: "cheats", label: `📄 Cheats (${categoryCounts.cheats || 6})` },
              ].map((cat) => {
                const isActive = activeCategory === cat.key;
                return (
                  <button
                    key={cat.key}
                    onClick={(e) => {
                      e.stopPropagation();
                      setActiveCategory(cat.key as SectionCategory);
                    }}
                    className={`px-3 py-1 rounded-full text-[11px] font-bold tracking-wide transition-all whitespace-nowrap cursor-pointer ${
                      isActive
                        ? "bg-[#FFE862] text-[#18181b] shadow-[0_2px_10px_rgba(255,232,98,0.35)]"
                        : "bg-white/5 hover:bg-white/10 text-[#f7f1ed]/70 hover:text-white border border-white/5"
                    }`}
                  >
                    {cat.label}
                  </button>
                );
              })}
            </div>

            {/* Search Input Bar */}
            <div className="relative my-2 shrink-0">
              <input
                ref={searchInputRef}
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Type to filter 27 sections (e.g. CUDA, vLLM, DSA, RAG)..."
                className="w-full px-3.5 py-1.5 pl-8 text-xs bg-white/5 hover:bg-white/10 focus:bg-white/10 border border-white/10 focus:border-[#FFE862]/60 rounded-xl text-[#f7f1ed] placeholder-white/40 outline-none transition-all"
              />
              <span className="absolute left-2.5 top-1/2 -translate-y-1/2 text-xs opacity-50">
                🔍
              </span>
              {searchQuery && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setSearchQuery("");
                  }}
                  className="absolute right-2.5 top-1/2 -translate-y-1/2 text-xs opacity-60 hover:opacity-100 text-white cursor-pointer"
                >
                  ✕
                </button>
              )}
            </div>

            {/* Sections List / Grid */}
            <div className="flex-1 overflow-y-auto pr-1 space-y-1.5 custom-scrollbar min-h-0">
              {filteredSections.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-40 text-center text-white/50 text-xs">
                  <span className="text-2xl mb-1.5">🔍</span>
                  <p>No sections matching &quot;{searchQuery}&quot;</p>
                  <button
                    onClick={() => {
                      setSearchQuery("");
                      setActiveCategory("all");
                    }}
                    className="mt-2 text-[#FFE862] hover:underline cursor-pointer"
                  >
                    Reset filters
                  </button>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5">
                  {filteredSections.map((section, idx) => {
                    const isSelected = section.id === activeId;
                    return (
                      <SectionCard
                        key={section.id}
                        section={section}
                        index={idx}
                        isSelected={isSelected}
                        onClick={() => handleSelect(section.id)}
                      />
                    );
                  })}
                </div>
              )}
            </div>

            {/* Bottom Hint Footer */}
            <div className="pt-2 border-t border-white/5 flex items-center justify-between text-[10px] text-white/40 font-mono shrink-0">
              <span>27 Technical Sections</span>
              <span>
                <kbd className="px-1 py-0.5 rounded bg-white/10 text-white/70">M</kbd> toggle ·{" "}
                <kbd className="px-1 py-0.5 rounded bg-white/10 text-white/70">ESC</kbd> close
              </span>
            </div>
          </div>

          {/* Bottom Bar: Menu + Hamburger / Close Navigation */}
          <motion.div
            className="relative z-10 flex items-center justify-between w-full shrink-0 cursor-pointer select-none"
            onClick={(e) => {
              e.stopPropagation();
              setIsOpen(!isOpen);
            }}
            animate={{
              paddingLeft: isOpen ? 22 : 18,
              paddingRight: isOpen ? 22 : 18,
              paddingBottom: isOpen ? 12 : 0,
              height: 48,
            }}
            transition={{ duration: 0.6, ease }}
            style={{ alignItems: "center" }}
          >
            <motion.span
              className="text-[13px] font-black uppercase tracking-wider leading-none flex items-center gap-2"
              animate={{ color: isOpen ? "#f7f1ed" : "#1a1a1a" }}
              transition={{ duration: 0.3, ease }}
            >
              <span
                className="w-[7px] h-[7px] rounded-full inline-block"
                style={{
                  backgroundColor: isOpen ? "#f43f5e" : "#16a34a",
                  boxShadow: isOpen ? "0 0 8px #f43f5e" : "0 0 8px #16a34a",
                }}
              />
              {isOpen ? "Close Navigation" : "Menu"}
            </motion.span>

            <div className="relative w-[22px] h-[22px] flex items-center justify-center">
              <motion.span
                className="absolute block w-[17px] h-[2px] rounded-full"
                animate={{
                  rotate: isOpen ? 45 : 0,
                  y: isOpen ? 0 : -3,
                  backgroundColor: isOpen ? "#f7f1ed" : "#1a1a1a",
                }}
                transition={{ duration: 0.35, ease }}
              />
              <motion.span
                className="absolute block w-[17px] h-[2px] rounded-full"
                animate={{
                  rotate: isOpen ? -45 : 0,
                  y: isOpen ? 0 : 3,
                  backgroundColor: isOpen ? "#f7f1ed" : "#1a1a1a",
                }}
                transition={{ duration: 0.35, ease }}
              />
            </div>
          </motion.div>
        </motion.div>
      </motion.div>
    </>
  );
}

// Individual Section Card inside Menu with Kinetic Split-Flap Char Roll
function SectionCard({
  section,
  index,
  isSelected,
  onClick,
}: {
  section: RoadmapSection;
  index: number;
  isSelected: boolean;
  onClick: () => void;
}) {
  const [hovered, setHovered] = useState(false);

  const categoryBadgeColors: Record<string, string> = {
    switch: "bg-orange-500/20 text-orange-400 border-orange-500/30",
    core: "bg-indigo-500/20 text-indigo-300 border-indigo-500/30",
    plans: "bg-teal-500/20 text-teal-300 border-teal-500/30",
    dsa: "bg-pink-500/20 text-pink-300 border-pink-500/30",
    prep: "bg-amber-500/20 text-amber-300 border-amber-500/30",
    cheats: "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
  };

  const badgeClass =
    categoryBadgeColors[section.cat] || "bg-white/10 text-white/70 border-white/10";

  return (
    <motion.button
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, delay: Math.min(index * 0.02, 0.2) }}
      className={`group w-full flex items-center justify-between gap-2.5 px-3 py-2 rounded-xl text-left transition-all duration-200 cursor-pointer border select-none ${
        isSelected
          ? "bg-indigo-600/30 border-indigo-500 shadow-[0_0_15px_rgba(99,102,241,0.25)]"
          : "bg-white/[0.04] hover:bg-[#FFE862]/10 border-white/[0.08] hover:border-[#FFE862]/40"
      }`}
    >
      <div className="flex items-center gap-2.5 min-w-0 flex-1">
        <span className="text-[10px] font-mono font-bold text-white/40 shrink-0 w-4">
          {String(index + 1).padStart(2, "0")}
        </span>
        <span className="text-sm shrink-0">{section.icon || "📄"}</span>
        <div className="flex flex-col min-w-0 flex-1">
          <div className="text-xs font-bold text-[#f7f1ed] truncate">
            <KineticCharRoll text={section.title} hovered={hovered} />
          </div>
          <span
            className={`text-[9px] font-mono uppercase px-1.5 py-0.2 rounded border w-fit tracking-wider mt-0.5 ${badgeClass}`}
          >
            {section.cat}
          </span>
        </div>
      </div>

      <div className="shrink-0 flex items-center">
        {isSelected ? (
          <span className="text-xs text-emerald-400 font-bold flex items-center gap-1 font-mono">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_6px_#34d399]" />
            ✓
          </span>
        ) : (
          <span className="text-xs text-white/30 group-hover:text-[#FFE862] group-hover:translate-x-0.5 transition-all">
            →
          </span>
        )}
      </div>
    </motion.button>
  );
}
