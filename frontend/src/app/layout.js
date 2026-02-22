import "./globals.css";
import { Cormorant_Garamond, Outfit } from "next/font/google";

const cormorant = Cormorant_Garamond({
    subsets: ["latin"],
    weight: ["300", "400", "500", "600", "700"],
    variable: "--font-cormorant"
});

const outfit = Outfit({
    subsets: ["latin"],
    variable: "--font-outfit"
});

export const metadata = {
    title: "NYU Course Search",
    description: "Semantic semantic search engine for NYU courses powered by AI embeddings.",
};

export default function RootLayout({ children }) {
    return (
        <html lang="en" className={`${cormorant.variable} ${outfit.variable}`}>
            <body className="font-sans antialiased bg-[#FAF9F6] text-neutral-900 selection:bg-[#57068c] selection:text-white min-h-screen flex flex-col">
                {children}
            </body>
        </html>
    );
}
