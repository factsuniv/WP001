#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for THPU White Paper System
Tests all API endpoints for the revolutionary THPU white paper backend
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, List, Any
import uuid

# Backend URL from frontend/.env
BACKEND_URL = "https://9ff8b068-b843-42e4-987f-d68282246334.preview.emergentagent.com/api"

class THPUBackendTester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_result(self, test_name: str, status: str, details: str = ""):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        self.total_tests += 1
        
        if status == "PASS":
            self.passed_tests += 1
            print(f"✅ {test_name}: {status}")
        else:
            self.failed_tests += 1
            print(f"❌ {test_name}: {status}")
            if details:
                print(f"   Details: {details}")
    
    def test_basic_api_connection(self):
        """Test GET /api/ endpoint for basic API connection"""
        try:
            response = requests.get(f"{BACKEND_URL}/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "THPU White Paper API" in data["message"]:
                    self.log_result("Basic API Connection", "PASS", 
                                  f"API responded with: {data}")
                else:
                    self.log_result("Basic API Connection", "FAIL", 
                                  f"Unexpected response format: {data}")
            else:
                self.log_result("Basic API Connection", "FAIL", 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Basic API Connection", "FAIL", f"Exception: {str(e)}")
    
    def test_whitepaper_endpoint(self):
        """Test GET /api/whitepaper endpoint to retrieve the revolutionary THPU white paper"""
        try:
            response = requests.get(f"{BACKEND_URL}/whitepaper", timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate white paper structure
                required_fields = ["id", "title", "abstract", "authors", "keywords", "sections", "references"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_result("White Paper Retrieval", "FAIL", 
                                  f"Missing required fields: {missing_fields}")
                    return
                
                # Validate title contains THPU
                if "Temporal-Holographic Processing Units" not in data["title"]:
                    self.log_result("White Paper Retrieval", "FAIL", 
                                  f"Title doesn't contain THPU: {data['title']}")
                    return
                
                # Validate 8 sections
                if len(data["sections"]) != 8:
                    self.log_result("White Paper Retrieval", "FAIL", 
                                  f"Expected 8 sections, got {len(data['sections'])}")
                    return
                
                # Validate section titles
                expected_sections = [
                    "Introduction", "Background", "Architecture", "Theoretical Foundations",
                    "Performance Analysis", "Implementation Roadmap", "Applications", "Conclusion"
                ]
                
                section_titles = [section["title"] for section in data["sections"]]
                for expected in expected_sections:
                    if not any(expected in title for title in section_titles):
                        self.log_result("White Paper Retrieval", "FAIL", 
                                      f"Missing expected section: {expected}")
                        return
                
                # Validate authors
                if len(data["authors"]) < 3:
                    self.log_result("White Paper Retrieval", "FAIL", 
                                  f"Expected at least 3 authors, got {len(data['authors'])}")
                    return
                
                # Validate references
                if len(data["references"]) < 5:
                    self.log_result("White Paper Retrieval", "FAIL", 
                                  f"Expected at least 5 references, got {len(data['references'])}")
                    return
                
                # Validate performance projections in content
                content_text = " ".join([section["content"] for section in data["sections"]])
                if "1000x energy efficiency" not in content_text or "100x throughput" not in content_text:
                    self.log_result("White Paper Retrieval", "FAIL", 
                                  "Missing performance projections (1000x energy efficiency, 100x throughput)")
                    return
                
                # Validate SVG diagrams in figures
                has_svg = False
                for section in data["sections"]:
                    for figure in section.get("figures", []):
                        if figure.get("svg_content") and "<svg" in figure["svg_content"]:
                            has_svg = True
                            break
                    if has_svg:
                        break
                
                if not has_svg:
                    self.log_result("White Paper Retrieval", "FAIL", 
                                  "No SVG diagrams found in figures")
                    return
                
                self.log_result("White Paper Retrieval", "PASS", 
                              f"Retrieved complete THPU white paper with {len(data['sections'])} sections, "
                              f"{len(data['authors'])} authors, {len(data['references'])} references")
                
            else:
                self.log_result("White Paper Retrieval", "FAIL", 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("White Paper Retrieval", "FAIL", f"Exception: {str(e)}")
    
    def test_presentation_endpoint(self):
        """Test GET /api/presentation endpoint to retrieve the presentation deck"""
        try:
            response = requests.get(f"{BACKEND_URL}/presentation", timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate presentation structure
                required_fields = ["id", "title", "description", "slides", "white_paper_id"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_result("Presentation Retrieval", "FAIL", 
                                  f"Missing required fields: {missing_fields}")
                    return
                
                # Validate 12 slides
                if len(data["slides"]) != 12:
                    self.log_result("Presentation Retrieval", "FAIL", 
                                  f"Expected 12 slides, got {len(data['slides'])}")
                    return
                
                # Validate slide structure
                for i, slide in enumerate(data["slides"]):
                    required_slide_fields = ["id", "title", "content", "slide_type", "order"]
                    missing_slide_fields = [field for field in required_slide_fields if field not in slide]
                    
                    if missing_slide_fields:
                        self.log_result("Presentation Retrieval", "FAIL", 
                                      f"Slide {i+1} missing fields: {missing_slide_fields}")
                        return
                
                # Validate title contains THPU
                if "THPU" not in data["title"]:
                    self.log_result("Presentation Retrieval", "FAIL", 
                                  f"Title doesn't contain THPU: {data['title']}")
                    return
                
                # Validate slide content contains key concepts (case-insensitive)
                all_content = " ".join([slide["content"] for slide in data["slides"]]).lower()
                key_concepts = ["temporal-holographic", "1000x", "100x", "energy efficiency", "throughput"]
                
                for concept in key_concepts:
                    if concept not in all_content:
                        self.log_result("Presentation Retrieval", "FAIL", 
                                      f"Missing key concept in slides: {concept}")
                        return
                
                self.log_result("Presentation Retrieval", "PASS", 
                              f"Retrieved complete THPU presentation with {len(data['slides'])} slides")
                
            else:
                self.log_result("Presentation Retrieval", "FAIL", 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Presentation Retrieval", "FAIL", f"Exception: {str(e)}")
    
    def test_whitepaper_sections_endpoint(self):
        """Test GET /api/whitepaper/sections endpoint to get all paper sections"""
        try:
            response = requests.get(f"{BACKEND_URL}/whitepaper/sections", timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate it's a list
                if not isinstance(data, list):
                    self.log_result("White Paper Sections", "FAIL", 
                                  f"Expected list, got {type(data)}")
                    return
                
                # Validate 8 sections
                if len(data) != 8:
                    self.log_result("White Paper Sections", "FAIL", 
                                  f"Expected 8 sections, got {len(data)}")
                    return
                
                # Validate section structure
                for i, section in enumerate(data):
                    required_fields = ["id", "title", "content", "order"]
                    missing_fields = [field for field in required_fields if field not in section]
                    
                    if missing_fields:
                        self.log_result("White Paper Sections", "FAIL", 
                                      f"Section {i+1} missing fields: {missing_fields}")
                        return
                
                # Validate sections are ordered
                orders = [section["order"] for section in data]
                if orders != sorted(orders):
                    self.log_result("White Paper Sections", "FAIL", 
                                  f"Sections not properly ordered: {orders}")
                    return
                
                # Validate substantial content in each section
                for section in data:
                    if len(section["content"]) < 500:  # Minimum content length
                        self.log_result("White Paper Sections", "FAIL", 
                                      f"Section '{section['title']}' has insufficient content")
                        return
                
                self.log_result("White Paper Sections", "PASS", 
                              f"Retrieved {len(data)} properly structured sections")
                
            else:
                self.log_result("White Paper Sections", "FAIL", 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("White Paper Sections", "FAIL", f"Exception: {str(e)}")
    
    def test_whitepaper_references_endpoint(self):
        """Test GET /api/whitepaper/references endpoint to get all references"""
        try:
            response = requests.get(f"{BACKEND_URL}/whitepaper/references", timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate it's a list
                if not isinstance(data, list):
                    self.log_result("White Paper References", "FAIL", 
                                  f"Expected list, got {type(data)}")
                    return
                
                # Validate at least 5 references
                if len(data) < 5:
                    self.log_result("White Paper References", "FAIL", 
                                  f"Expected at least 5 references, got {len(data)}")
                    return
                
                # Validate reference structure
                for i, ref in enumerate(data):
                    required_fields = ["id", "title", "authors", "journal", "year"]
                    missing_fields = [field for field in required_fields if field not in ref]
                    
                    if missing_fields:
                        self.log_result("White Paper References", "FAIL", 
                                      f"Reference {i+1} missing fields: {missing_fields}")
                        return
                
                # Validate UUIDs are used instead of MongoDB ObjectIDs
                for ref in data:
                    ref_id = ref["id"]
                    try:
                        uuid.UUID(ref_id)
                    except ValueError:
                        self.log_result("White Paper References", "FAIL", 
                                      f"Reference ID is not a valid UUID: {ref_id}")
                        return
                
                # Validate reference years are reasonable
                for ref in data:
                    year = ref["year"]
                    if not isinstance(year, int) or year < 2020 or year > 2025:
                        self.log_result("White Paper References", "FAIL", 
                                      f"Invalid reference year: {year}")
                        return
                
                self.log_result("White Paper References", "PASS", 
                              f"Retrieved {len(data)} properly formatted references with UUIDs")
                
            else:
                self.log_result("White Paper References", "FAIL", 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("White Paper References", "FAIL", f"Exception: {str(e)}")
    
    def test_mongodb_integration(self):
        """Test MongoDB integration by making multiple requests to verify data persistence"""
        try:
            # Make two requests to the same endpoint
            response1 = requests.get(f"{BACKEND_URL}/whitepaper", timeout=30)
            response2 = requests.get(f"{BACKEND_URL}/whitepaper", timeout=30)
            
            if response1.status_code == 200 and response2.status_code == 200:
                data1 = response1.json()
                data2 = response2.json()
                
                # Verify data consistency
                if data1["id"] == data2["id"] and data1["title"] == data2["title"]:
                    self.log_result("MongoDB Integration", "PASS", 
                                  "Data persistence verified - consistent responses")
                else:
                    self.log_result("MongoDB Integration", "FAIL", 
                                  "Data inconsistency between requests")
            else:
                self.log_result("MongoDB Integration", "FAIL", 
                              f"Failed to get consistent responses: {response1.status_code}, {response2.status_code}")
                
        except Exception as e:
            self.log_result("MongoDB Integration", "FAIL", f"Exception: {str(e)}")
    
    def test_api_response_format(self):
        """Test that all API responses follow proper JSON structure"""
        endpoints = [
            ("/", "Basic API"),
            ("/whitepaper", "White Paper"),
            ("/presentation", "Presentation"),
            ("/whitepaper/sections", "Sections"),
            ("/whitepaper/references", "References")
        ]
        
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=30)
                
                if response.status_code == 200:
                    # Verify it's valid JSON
                    try:
                        data = response.json()
                        
                        # Verify proper content type
                        content_type = response.headers.get('content-type', '')
                        if 'application/json' not in content_type:
                            self.log_result(f"JSON Format - {name}", "FAIL", 
                                          f"Wrong content type: {content_type}")
                            continue
                        
                        # Verify no MongoDB ObjectIDs in response
                        response_text = json.dumps(data)
                        if '"_id"' in response_text or 'ObjectId' in response_text:
                            self.log_result(f"JSON Format - {name}", "FAIL", 
                                          "Response contains MongoDB ObjectIDs")
                            continue
                        
                        self.log_result(f"JSON Format - {name}", "PASS", 
                                      "Proper JSON structure with UUIDs")
                        
                    except json.JSONDecodeError as e:
                        self.log_result(f"JSON Format - {name}", "FAIL", 
                                      f"Invalid JSON: {str(e)}")
                        
                else:
                    self.log_result(f"JSON Format - {name}", "FAIL", 
                                  f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_result(f"JSON Format - {name}", "FAIL", f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all backend API tests"""
        print("🚀 Starting THPU White Paper Backend API Testing")
        print("=" * 60)
        
        # Test basic connectivity first
        self.test_basic_api_connection()
        
        # Test main endpoints
        self.test_whitepaper_endpoint()
        self.test_presentation_endpoint()
        self.test_whitepaper_sections_endpoint()
        self.test_whitepaper_references_endpoint()
        
        # Test system integration
        self.test_mongodb_integration()
        self.test_api_response_format()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        if self.failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.results:
                if result["status"] == "FAIL":
                    print(f"  - {result['test']}: {result['details']}")
        
        return self.failed_tests == 0

if __name__ == "__main__":
    tester = THPUBackendTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! THPU Backend API is working correctly.")
        sys.exit(0)
    else:
        print(f"\n💥 {tester.failed_tests} test(s) failed. Please check the issues above.")
        sys.exit(1)