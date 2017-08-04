package geowave.util;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.regex.Pattern;

import static org.junit.Assert.*;


public class TestUtils {
	// To make tests cleaner.  See SO https://stackoverflow.com/questions/86780/
	public static boolean insensitiveMatch(String fullString, String targetString) {
		Pattern p = Pattern.compile(Pattern.quote(targetString), Pattern.CASE_INSENSITIVE);
		return p.matcher(fullString).find();
	}
	
	// Assert that the response was successful
	public static void assertSuccess(String response) {
		assertNotNull("Response should not be null", response);
		if (insensitiveMatch(response, "exception")) {
			System.out.println("R: " + response);
			fail("Response should not contain exception");
		} else {
			// pass
		}
// 		TODO: put this back
//		assertTrue("Response should not contain error", !insensitiveMatch(response, "error"));
	}
	
	// Return the status code from a GET
	public static int get(String url) {
		try {
			URL u = new URL(url);
			HttpURLConnection c = (HttpURLConnection) u.openConnection();
			c.setRequestMethod("HEAD");
			c.connect();
			int code = c.getResponseCode();
			return code;
		} catch (IOException e) {
			return 0;
		}
	}
	
	// Wait until URL returns 200
	public static boolean tryUntilOK(String url, int timeoutSeconds) {
		while (timeoutSeconds >= 0) {
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				assert false;
			}
			
			if (get(url) == 200) {
				return true;
			}
			timeoutSeconds--;
		}
		return false;
	}
	
}
