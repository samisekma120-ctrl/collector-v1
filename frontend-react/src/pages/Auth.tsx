import { useState } from "react";
import { apiFetch, setToken } from "../lib/api";
import type { TokenResponse, UserRole } from "../lib/types";

export default function Auth() {
  const [regEmail, setRegEmail] = useState("");
  const [regPass, setRegPass] = useState("Test1234!");
  const [regRole, setRegRole] = useState<UserRole>("buyer");

  const [logEmail, setLogEmail] = useState("");
  const [logPass, setLogPass] = useState("Test1234!");

  const [msg, setMsg] = useState<string>("");

  async function register() {
    setMsg("");
    try {
      await apiFetch("/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: regEmail, password: regPass, role: regRole }),
      });
      setMsg("✅ Compte créé. Tu peux te connecter.");
    } catch (e: any) {
      setMsg(`❌ Erreur register: ${JSON.stringify(e.body ?? e)}`);
    }
  }

  async function login() {
    setMsg("");
    try {
      const data = await apiFetch<TokenResponse>("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: logEmail, password: logPass }),
      });
      setToken(data.access_token);
      setMsg("✅ Connecté. Va dans “Espace” ou “Admin”.");
    } catch (e: any) {
      setMsg(`❌ Erreur login: ${JSON.stringify(e.body ?? e)}`);
    }
  }

  return (
    <>
      <div className="row">
        <div className="col card">
          <h2 style={{ marginTop: 0 }}>Créer un compte</h2>
          <label>Email</label>
          <input value={regEmail} onChange={(e) => setRegEmail(e.target.value)} placeholder="buyer@example.com" />
          <label>Mot de passe</label>
          <input value={regPass} onChange={(e) => setRegPass(e.target.value)} type="password" />
          <label>Rôle</label>
          <select value={regRole} onChange={(e) => setRegRole(e.target.value as UserRole)}>
            <option value="buyer">Acheteur</option>
            <option value="seller">Vendeur</option>
            <option value="admin">Admin</option>
          </select>
          <button onClick={register}>Créer</button>
        </div>

        <div className="col card">
          <h2 style={{ marginTop: 0 }}>Connexion</h2>
          <label>Email</label>
          <input value={logEmail} onChange={(e) => setLogEmail(e.target.value)} placeholder="admin@example.com" />
          <label>Mot de passe</label>
          <input value={logPass} onChange={(e) => setLogPass(e.target.value)} type="password" />
          <button onClick={login}>Se connecter</button>
        </div>
      </div>

      <div className="card">
        <h2 style={{ marginTop: 0 }}>Message</h2>
        <div className="small">{msg || "—"}</div>
      </div>
    </>
  );
}
