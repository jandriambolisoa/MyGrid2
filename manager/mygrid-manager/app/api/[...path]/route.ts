import { NextRequest, NextResponse } from "next/server";

const API_URL = process.env.API_URL!;

export async function GET(req: NextRequest) {
  return handleRequest(req, "GET");
}

export async function POST(req: NextRequest) {
  return handleRequest(req, "POST");
}

export async function PUT(req: NextRequest) {
  return handleRequest(req, "PUT");
}

export async function DELETE(req: NextRequest) {
  return handleRequest(req, "DELETE");
}

async function handleRequest(req: NextRequest, method: string) {

  const token = req.cookies.get("token")?.value;
  const url = `${API_URL}${req.nextUrl.pathname.replace("/api", "")}${req.nextUrl.search}`;
  let body: string | undefined;

  if (method !== "GET") {
    body = await req.text();
  }

  const response = await fetch(url, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
    },
    ...(body ? { body } : {})
  });

  const data = await response.json();

  if (!response.ok) {
    return NextResponse.json({ error: data.detail || "Request failed" }, { status: response.status });
  }

  return NextResponse.json(data);

}