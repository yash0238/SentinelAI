import "./globals.css";
import Sidebar from "@/components/Sidebar";

export const metadata = {
  title: "SentinelAI — Law Enforcement Dashboard",
  description: "Proactive Intelligence for Digital Public Safety & Fraud Neutralisation",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-base-900 text-slate-100 min-h-screen flex selection:bg-accent-blue/30 selection:text-white">
        <Sidebar />
        <main className="flex-1 ml-[230px] p-6 lg:p-8 transition-all duration-300">
          <div className="max-w-7xl mx-auto h-full flex flex-col">
            {children}
          </div>
        </main>
      </body>
    </html>
  );
}
