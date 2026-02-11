import { Link, NavLink, Route, Routes } from "react-router-dom";
import Catalogue from "./pages/Catalogue";
import Auth from "./pages/Auth";
import Me from "./pages/Me";
import Admin from "./pages/Admin";

export default function App() {
  return (
    <div style={{ fontFamily: "system-ui", maxWidth: 980, margin: "0 auto", padding: 24 }}>
      <header style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", gap: 16 }}>
        <div>
          <h1 style={{ margin: 0 }}>Collector V1</h1>
          <div style={{ opacity: 0.75 }}>Démo : catalogue public + auth + back-office admin (catégories)</div>
        </div>
        <nav style={{ display: "flex", gap: 12 }}>
          <NavLink to="/" end>Catalogue</NavLink>
          <NavLink to="/auth">Auth</NavLink>
          <NavLink to="/me">Espace</NavLink>
          <NavLink to="/admin">Admin</NavLink>
        </nav>
      </header>

      <main style={{ marginTop: 18 }}>
        <Routes>
          <Route path="/" element={<Catalogue />} />
          <Route path="/auth" element={<Auth />} />
          <Route path="/me" element={<Me />} />
          <Route path="/admin" element={<Admin />} />
          <Route path="*" element={<div>404 — <Link to="/">retour</Link></div>} />
        </Routes>
      </main>
    </div>
  );
}
