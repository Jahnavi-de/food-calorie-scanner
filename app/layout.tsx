import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Food Calorie Scanner",
  description: "Scan food images and estimate calories with BMI guidance"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
