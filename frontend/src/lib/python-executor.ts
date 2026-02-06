/**
 * Python API Service
 * Provides a robust interface for communicating with Python services
 * Designed for serverless environments where direct process spawning is not allowed
 */

interface PythonExecutionResult {
  success: boolean;
  data?: any;
  error?: string;
}

class PythonApiService {
  /**
   * Execute a Python function via HTTP API (recommended for serverless environments)
   */
  async executeViaHttpApi(
    apiUrl: string,
    payload: any
  ): Promise<PythonExecutionResult> {
    console.log(`Making HTTP request to Python API: ${apiUrl}`, payload);

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add any required authentication headers here
          ...(process.env.PYTHON_API_KEY ? { 'Authorization': `Bearer ${process.env.PYTHON_API_KEY}` } : {}),
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorMsg = `HTTP ${response.status}: ${response.statusText}`;
        console.error('Python API request failed:', errorMsg);

        // Check for rate limiting errors
        if (response.status === 429) {
          return {
            success: false,
            error: "Rate limit exceeded. Please try again later."
          };
        }

        return {
          success: false,
          error: errorMsg
        };
      }

      const data = await response.json();
      console.log('Python API response received successfully');
      return {
        success: true,
        data
      };
    } catch (error: any) {
      console.error('Python API request error:', error?.message || error);
      return {
        success: false,
        error: error?.message || String(error)
      };
    }
  }
}

// Singleton instance
const pythonApiService = new PythonApiService();

export { pythonApiService };
export type { PythonApiService, PythonExecutionResult };