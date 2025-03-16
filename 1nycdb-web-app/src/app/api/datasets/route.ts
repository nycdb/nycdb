// Connect API endpoints to the data access layer

import { NextRequest, NextResponse } from 'next/server';
import { getAllDatasets } from '../../../lib/data-access';

// GET /api/datasets - Get all available datasets
export async function GET(request: NextRequest) {
  try {
    // Call the data access function
    const result = await getAllDatasets();
    
    if (!result.success) {
      return NextResponse.json(
        { error: result.error || 'Error retrieving datasets' },
        { status: 400 }
      );
    }
    
    // Return simplified dataset info for the frontend
    const simplifiedDatasets = result.data.map(dataset => ({
      id: dataset.id,
      name: dataset.name,
      description: dataset.description,
      category: dataset.category
    }));
    
    return NextResponse.json(simplifiedDatasets);
  } catch (error) {
    console.error('Error in datasets API:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
