"use client";
import { useState } from "react";

export default function Login() {
    const [email, setEmail] = useState("");
    const [error, setError] = useState("");

    const handleLogin = (e) => {
        e.preventDefault();
        if (!email.endsWith("@nyu.edu")) {
            setError("Please use a valid @nyu.edu email address.");
            return;
        }
        // Pre-authorized or mock login success
        setError("");
        window.location.href = "/";
    };

    return (
        <div className="min-h-screen bg-neutral-50 flex flex-col items-center justify-center p-4">
            <div className="max-w-md w-full bg-white p-8 rounded-2xl shadow-sm border border-neutral-100 text-center">
                <div className="w-16 h-16 bg-[#57068c] rounded-2xl mx-auto mb-6 flex items-center justify-center">
                    <span className="text-white font-bold text-2xl">N</span>
                </div>

                <h1 className="text-2xl font-bold text-neutral-900 mb-2">NYU Course Search</h1>
                <p className="text-neutral-500 mb-8">Sign in with your university account to plan your semesters and search courses.</p>

                <form onSubmit={handleLogin} className="space-y-4">
                    <div>
                        <input
                            type="email"
                            required
                            className="w-full p-3 rounded-xl border border-neutral-200 outline-none focus:ring-2 focus:ring-[#57068c]/20 focus:border-[#57068c] transition-all"
                            placeholder="netid@nyu.edu"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>

                    {error && <p className="text-red-500 text-sm font-medium text-left">{error}</p>}

                    <button
                        type="submit"
                        className="w-full bg-[#57068c] text-white p-3 rounded-xl font-medium hover:bg-[#43046b] transition-colors"
                    >
                        Continue with Email
                    </button>
                </form>

                <p className="mt-8 text-xs text-neutral-400">
                    This system is restricted to verified New York University students.
                </p>
            </div>
        </div>
    );
}
