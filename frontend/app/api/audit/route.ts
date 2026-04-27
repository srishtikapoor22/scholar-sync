import { NextResponse } from 'next/server';

const BACKEND_AUDIT_URL = process.env.BACKEND_AUDIT_URL ?? 'http://localhost:8000/audit?pdf=testdoc.pdf';

export const runtime = 'nodejs';

export async function GET() {
  try {
    const response = await fetch(BACKEND_AUDIT_URL, {
      headers: {
        Accept: 'text/event-stream',
      },
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: 'Failed to fetch from backend' },
        { status: response.status },
      );
    }

    return new NextResponse(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache, no-transform',
        Connection: 'keep-alive',
      },
    });
  } catch (error) {
    console.error('Audit API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 },
    );
  }
}

