// API endpoint for dataset details

import { NextRequest, NextResponse } from 'next/server';
import { getDatasetById } from '../../schema';

// GET /api/datasets/:id - Get dataset details
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const dataset = getDatasetById(params.id);
  
  if (!dataset) {
    return NextResponse.json(
      { error: 'Dataset not found' },
      { status: 404 }
    );
  }
  
  return NextResponse.json(dataset);
}
