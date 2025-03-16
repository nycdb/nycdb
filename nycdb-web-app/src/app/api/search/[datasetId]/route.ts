// Connect API endpoints to the data access layer

import { NextRequest, NextResponse } from 'next/server';
import { searchDataset } from '../../../lib/data-access';

// GET /api/search/:datasetId - Search within a dataset
export async function GET(
  request: NextRequest,
  { params }: { params: { datasetId: string } }
) {
  try {
    // Get search parameters from URL
    const searchParams = request.nextUrl.searchParams;
    const query = searchParams.get('query') || '';
    const field = searchParams.get('field') || '';
    const page = parseInt(searchParams.get('page') || '1', 10);
    const limit = parseInt(searchParams.get('limit') || '20', 10);
    
    // Call the data access function
    const result = await searchDataset(params.datasetId, {
      query,
      field,
      page,
      limit
    });
    
    if (!result.success) {
      return NextResponse.json(
        { error: result.error || 'Error searching dataset' },
        { status: 400 }
      );
    }
    
    return NextResponse.json(result.data);
  } catch (error) {
    console.error('Error in search API:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
