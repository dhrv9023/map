import FloatingMenu from "@/components/ui/liquid-morph-floating-menu";

declare global {
  interface Window {
    show?: (id: string) => void;
    toggleDarkMode?: () => void;
    openSearchModal?: () => void;
  }
}

export default function App() {
  const items = [
    {
      label: "CAREER SWITCH",
      onClick: () => {
        window.show?.("s25");
      },
    },
    {
      label: "CORE CURRICULUM",
      onClick: () => {
        window.show?.("s1");
      },
    },
    {
      label: "DAY PLANS",
      onClick: () => {
        window.show?.("s11");
      },
    },
    {
      label: "DSA & DESIGN",
      onClick: () => {
        window.show?.("s6");
      },
    },
    {
      label: "PROJECTS & PREP",
      onClick: () => {
        window.show?.("s8");
      },
    },
    {
      label: "CHEATS & SCHEDULE",
      onClick: () => {
        window.show?.("s26");
      },
    },
    {
      label: "SEARCH (CMD+K)",
      onClick: () => {
        window.openSearchModal?.();
      },
    },
    {
      label: "TOGGLE THEME",
      onClick: () => {
        window.toggleDarkMode?.();
      },
    },
  ];

  return <FloatingMenu items={items} />;
}
