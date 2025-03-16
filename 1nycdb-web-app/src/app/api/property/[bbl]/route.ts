// Connect API endpoints to the data access layer

import { NextRequest, NextResponse } from 'next/server';
import { getPropertyByBBL } from '../../../lib/data-access';

// GET /api/property/:bbl - Get all info for a specific property by BBL
export async function GET(
  request: NextRequest,
  { params }: { params: { bbl: string } }
) {
  try {
    const bbl = params.bbl;
    
    // Call the data access function
    const result = await getPropertyByBBL(bbl);
    
    if (!result.success) {
      return NextResponse.json(
        { error: result.error || 'Error retrieving property information' },
        { status: 400 }
      );
    }
    
    return NextResponse.json(result.data);
  } catch (error) {
    console.error('Error in property API:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
