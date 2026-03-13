import { NextResponse } from "next/server";

export async function POST(req: Request) {

  const API_URL = process.env.API_URL;

  const {username, password} = await req.json();
  const data = await fetch(`${API_URL}/auth/login-email`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
  }).then(r => r.json());

  if (data.access_token) {
    const res = NextResponse.json({ success: true });
    res.cookies.set({
      name: "token",
      value: data.access_token,
      httpOnly: true,
      path: "/",
      maxAge: 60 * 60,
      sameSite: "strict",
      secure: process.env.NODE_ENV === "production",
    })
    return res
  }

  return NextResponse.json({ error: data.detail || "Login failed"}, { status: 400 });
}