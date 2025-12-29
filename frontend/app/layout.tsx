import type { Metadata } from "next";
import { Bebas_Neue, JetBrains_Mono, Playfair_Display } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";

const bebas = Bebas_Neue({ 
  weight: "400",
  subsets: ["latin"], 
  variable: "--font-bebas" 
});

const jetbrainsMono = JetBrains_Mono({ 
  subsets: ["latin"], 
  variable: "--font-mono" 
});

const playfair = Playfair_Display({ 
  subsets: ["latin"], 
  variable: "--font-serif" 
});

export const metadata: Metadata = {
  title: "The Trading Floor | AI Agent Council",
  description: "Multi-agent market analysis dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={cn(
        bebas.variable,
        jetbrainsMono.variable,
        playfair.variable,
        "bg-background text-text-primary antialiased min-h-screen selection:bg-gold-primary selection:text-bg-primary"
      )}>
        <div className="art-deco-pattern" />
        <div className="scanline" />
        {children}
      </body>
    </html>
  );
}
