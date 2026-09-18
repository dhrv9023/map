import FloatingMenu, { ALL_SECTIONS } from "@/components/ui/liquid-morph-floating-menu";

declare global {
  interface Window {
    show?: (id: string, btn?: HTMLElement | null) => void;
    toggleDarkMode?: () => void;
    openSearchModal?: () => void;
  }
}

export default function App() {
  const handleSelectSection = (id: string) => {
    if (id === "s6") {
      window.location.href = "./dsa/index.html";
      return;
    }
    if (window.show) {
      window.show(id);
    }
  };

  return (
    <FloatingMenu
      sections={ALL_SECTIONS}
      onSelectSection={handleSelectSection}
    />
  );
}
