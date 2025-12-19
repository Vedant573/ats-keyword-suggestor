#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATS Keyword Suggestor & JD Optimizer
A GUI application for analyzing resumes against job descriptions
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import PyPDF2
import re
import json
import subprocess
import os
from pathlib import Path


class ATSKeywordSuggestorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ATS Keyword Suggestor & JD Optimizer")
        self.root.geometry("1000x800")
        
        # Variables
        self.resume_file = None
        self.resume_content = ""
        self.resume_format = None
        self.api_key = tk.StringVar()
        self.jd_text = tk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title = ttk.Label(main_frame, text="ATS Keyword Suggestor & JD Optimizer", 
                         font=('Helvetica', 16, 'bold'))
        title.grid(row=0, column=0, pady=10)
        
        # API Key Section
        api_frame = ttk.LabelFrame(main_frame, text="Optional: AI Configuration (for smart suggestions)", padding="10")
        api_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        api_frame.columnconfigure(1, weight=1)
        
        # API Provider Selection
        ttk.Label(api_frame, text="API Provider:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.api_provider = tk.StringVar(value="openai")
        provider_combo = ttk.Combobox(api_frame, textvariable=self.api_provider, 
                                      values=["openai", "anthropic", "google", "custom"], 
                                      state="readonly", width=20)
        provider_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(api_frame, text="API Key:").grid(row=1, column=0, sticky=tk.W, padx=5)
        api_entry = ttk.Entry(api_frame, textvariable=self.api_key, show="*", width=50)
        api_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        # Custom API URL (for custom providers)
        ttk.Label(api_frame, text="Custom API URL:").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.custom_api_url = tk.StringVar()
        custom_url_entry = ttk.Entry(api_frame, textvariable=self.custom_api_url, width=50)
        custom_url_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        ttk.Label(api_frame, text="Model (optional):").grid(row=3, column=0, sticky=tk.W, padx=5)
        self.model_name = tk.StringVar()
        model_entry = ttk.Entry(api_frame, textvariable=self.model_name, width=50)
        model_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        # Resume Upload Section
        upload_frame = ttk.LabelFrame(main_frame, text="Step 1: Resume Upload", padding="10")
        upload_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        upload_frame.columnconfigure(1, weight=1)
        
        ttk.Button(upload_frame, text="Select Resume (.tex or .pdf)", 
                  command=self.load_resume).grid(row=0, column=0, padx=5)
        self.file_label = ttk.Label(upload_frame, text="No file selected", foreground="gray")
        self.file_label.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Resume Preview Section
        preview_frame = ttk.LabelFrame(main_frame, text="Resume Content Preview", padding="10")
        preview_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        self.resume_preview = scrolledtext.ScrolledText(preview_frame, height=10, wrap=tk.WORD)
        self.resume_preview.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Job Description Section
        jd_frame = ttk.LabelFrame(main_frame, text="Step 2: Paste Job Description", padding="10")
        jd_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        jd_frame.columnconfigure(0, weight=1)
        jd_frame.rowconfigure(0, weight=1)
        
        self.jd_text_widget = scrolledtext.ScrolledText(jd_frame, height=10, wrap=tk.WORD)
        self.jd_text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Action Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, pady=10)
        
        ttk.Button(button_frame, text="Step 3: Analyze & Suggest Keywords", 
                  command=self.suggest_keywords, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        # REMOVED: ttk.Button(button_frame, text="Auto-Apply Keywords & Generate .tex", command=self.auto_apply_keywords).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
        # Status Section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=5)
        status_frame.columnconfigure(0, weight=1)
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=6, wrap=tk.WORD, 
                                                     state='disabled')
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Configure row weights for resizing
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(4, weight=1)
    
    def log_status(self, message):
        self.status_text.config(state='normal')
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state='disabled')
        self.root.update()
    
    def load_resume(self):
        file_path = filedialog.askopenfilename(
            title="Select Resume",
            filetypes=[("LaTeX files", "*.tex"), ("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        self.resume_file = file_path
        self.file_label.config(text=os.path.basename(file_path), foreground="blue")
        
        # Determine file type and extract content
        if file_path.endswith('.tex'):
            self.resume_format = 'tex'
            self.resume_content = self.read_tex_file(file_path)
        elif file_path.endswith('.pdf'):
            self.resume_format = 'pdf'
            self.resume_content = self.read_pdf_file(file_path)
        else:
            messagebox.showerror("Error", "Unsupported file format. Please use .tex or .pdf")
            return
        
        # Display preview
        self.resume_preview.delete(1.0, tk.END)
        self.resume_preview.insert(1.0, self.resume_content[:2000] + "..." if len(self.resume_content) > 2000 else self.resume_content)
        
        self.log_status(f"✓ Resume loaded: {os.path.basename(file_path)} ({self.resume_format.upper()})")
    
    def read_tex_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read .tex file: {str(e)}")
            return ""
    
    def read_pdf_file(self, file_path):
        try:
            text = ""
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read PDF file: {str(e)}")
            return ""
    
    def extract_immutable_fields(self, content):
        """Extract fields that should remain unchanged"""
        fields = {}
        
        # Common patterns for contact info
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        phone_pattern = r'[\+\d][\d\-\(\)\s]{8,}'
        linkedin_pattern = r'linkedin\.com/[\w\-/]+'
        github_pattern = r'github\.com/[\w\-]+'
        
        emails = re.findall(email_pattern, content)
        phones = re.findall(phone_pattern, content)
        linkedin = re.findall(linkedin_pattern, content, re.IGNORECASE)
        github = re.findall(github_pattern, content, re.IGNORECASE)
        
        if emails:
            fields['email'] = emails[0]
        if phones:
            fields['phone'] = phones[0].strip()
        if linkedin:
            fields['linkedin'] = linkedin[0]
        if github:
            fields['github'] = github[0]
        
        # Extract name (first line or \name command in LaTeX)
        if self.resume_format == 'tex':
            name_match = re.search(r'\\name\{([^}]+)\}', content)
            if name_match:
                fields['name'] = name_match.group(1)
        else:
            lines = content.strip().split('\n')
            if lines:
                fields['name'] = lines[0].strip()
        
        return fields
    
    def suggest_keywords(self):
        if not self.resume_content:
            messagebox.showerror("Error", "Please load a resume first")
            return
        
        jd = self.jd_text_widget.get(1.0, tk.END).strip()
        if not jd:
            messagebox.showerror("Error", "Please enter a Job Description")
            return
        
        self.log_status("Analyzing resume and job description...")
        
        # Extract immutable fields
        immutable_fields = self.extract_immutable_fields(self.resume_content)
        self.log_status(f"✓ Extracted immutable fields: {', '.join(immutable_fields.keys())}")
        
        # Analyze without API if no key provided
        if not self.api_key.get():
            self.log_status("No API key provided. Using local keyword extraction...")
            keywords = self.extract_keywords_locally(self.resume_content, jd)
            self.display_keyword_suggestions(keywords, immutable_fields)
        else:
            # Call AI API for intelligent suggestions
            try:
                keywords = self.get_ai_keyword_suggestions(self.resume_content, jd, immutable_fields)
                self.display_keyword_suggestions(keywords, immutable_fields)
            except Exception as e:
                self.log_status(f"API Error: {str(e)}")
                self.log_status("Falling back to local keyword extraction...")
                keywords = self.extract_keywords_locally(self.resume_content, jd)
                self.display_keyword_suggestions(keywords, immutable_fields)
    
    def extract_keywords_locally(self, resume_content, jd):
        """Extract keywords locally without API"""
        import re
        from collections import Counter
        
        # Common technical skills patterns
        tech_keywords = []
        
        # Extract words from JD
        jd_words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b|\b[A-Z]+\b|\b\w+\b', jd)
        jd_lower = [w.lower() for w in jd_words]
        
        # Extract words from resume
        resume_words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b|\b[A-Z]+\b|\b\w+\b', resume_content)
        resume_lower = [w.lower() for w in resume_words]
        
        # Common stop words to ignore
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
                     'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 
                     'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that',
                     'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'}
        
        # Find keywords in JD that are NOT in resume
        missing_keywords = []
        word_freq = Counter(jd_lower)
        
        for word, count in word_freq.most_common(100):
            if (len(word) > 3 and 
                word not in stop_words and 
                word not in resume_lower and
                not word.isdigit()):
                missing_keywords.append(word.title())
        
        # Find technical terms (capitalized words, acronyms)
        tech_terms = set()
        for word in jd_words:
            if (len(word) > 2 and 
                (word.isupper() or word[0].isupper()) and 
                word.lower() not in stop_words):
                if word.lower() not in resume_lower:
                    tech_terms.add(word)
        
        # Find multi-word phrases
        jd_clean = re.sub(r'[^\w\s]', ' ', jd.lower())
        resume_clean = re.sub(r'[^\w\s]', ' ', resume_content.lower())
        
        bigrams = []
        words = jd_clean.split()
        for i in range(len(words) - 1):
            phrase = f"{words[i]} {words[i+1]}"
            if (phrase not in resume_clean and 
                words[i] not in stop_words and 
                words[i+1] not in stop_words and
                len(words[i]) > 2 and len(words[i+1]) > 2):
                bigrams.append(phrase.title())
        
        return {
            'missing_keywords': missing_keywords[:20],
            'technical_terms': list(tech_terms)[:15],
            'key_phrases': list(set(bigrams))[:15],
            'suggestions': {
                'skills': missing_keywords[:10],
                'experience': list(set(bigrams))[:8],
                'action_verbs': self.extract_action_verbs(jd)
            }
        }
    
    def extract_action_verbs(self, text):
        """Extract action verbs from job description"""
        common_action_verbs = [
            'developed', 'designed', 'implemented', 'created', 'built', 'managed',
            'led', 'coordinated', 'executed', 'delivered', 'achieved', 'improved',
            'optimized', 'analyzed', 'evaluated', 'collaborated', 'contributed',
            'established', 'maintained', 'enhanced', 'streamlined', 'automated',
            'integrated', 'deployed', 'architected', 'engineered', 'facilitated'
        ]
        
        text_lower = text.lower()
        found_verbs = []
        for verb in common_action_verbs:
            if verb in text_lower:
                found_verbs.append(verb.title())
        
        return found_verbs[:10]
    
    def get_ai_keyword_suggestions(self, resume_content, jd, immutable_fields):
        """Use AI API to get intelligent keyword suggestions"""
        self.log_status(f"Calling {self.api_provider.get().upper()} API for suggestions...")
        
        provider = self.api_provider.get()
        
        prompt = f"""Analyze this resume and job description. Provide keyword suggestions for manual optimization.

RESUME (keep unchanged):
{immutable_fields}

RESUME CONTENT:
{resume_content[:3000]}...

JOB DESCRIPTION:
{jd}

Provide suggestions in this EXACT JSON format:
{{
  "missing_keywords": ["keyword1", "keyword2", ...],
  "technical_terms": ["term1", "term2", ...],
  "key_phrases": ["phrase1", "phrase2", ...],
  "suggestions": {{
    "skills": ["skill1", "skill2", ...],
    "experience": ["accomplishment phrase1", ...],
    "action_verbs": ["verb1", "verb2", ...]
  }},
  "placement_tips": [
    "Where to add: specific section - keyword suggestion",
    ...
  ]
}}

Focus on keywords that naturally fit the resume without lying. Return ONLY the JSON, no other text."""

        try:
            if provider == "openai":
                response_text = self.call_openai_simple(prompt)
            elif provider == "anthropic":
                response_text = self.call_anthropic_simple(prompt)
            elif provider == "google":
                response_text = self.call_google_simple(prompt)
            elif provider == "custom":
                response_text = self.call_custom_api(prompt)
            else:
                raise ValueError(f"Unsupported API provider: {provider}")
            
            # Extract JSON from response
            import json
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # If no JSON found, parse as plain text
                return self.parse_text_suggestions(response_text)
        
        except Exception as e:
            self.log_status(f"API call failed: {str(e)}")
            raise
    
    def call_openai_simple(self, prompt):
        """Simplified OpenAI call for suggestions"""
        # NOTE: This requires the 'openai' library to be installed and configured
        try:
            import openai
        except ImportError:
            raise ImportError("The 'openai' library is not installed. Please install it with 'pip install openai'")
            
        openai.api_key = self.api_key.get()
        model = self.model_name.get() if self.model_name.get() else "gpt-3.5-turbo"
        
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a resume optimization expert. Return only JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1500
        )
        return response.choices[0].message.content
    
    def call_anthropic_simple(self, prompt):
        """Simplified Anthropic call for suggestions"""
        # NOTE: This requires the 'anthropic' library to be installed and configured
        try:
            import anthropic
        except ImportError:
            raise ImportError("The 'anthropic' library is not installed. Please install it with 'pip install anthropic'")

        client = anthropic.Anthropic(api_key=self.api_key.get())
        model = self.model_name.get() if self.model_name.get() else "claude-3-haiku-20240307"
        
        message = client.messages.create(
            model=model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    
    def call_google_simple(self, prompt):
        """Simplified Google call for suggestions"""
        # NOTE: This requires the 'google-genai' library to be installed and configured
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("The 'google-genai' library is not installed. Please install it with 'pip install google-genai'")

        genai.configure(api_key=self.api_key.get())
        model_name = self.model_name.get() if self.model_name.get() else "gemini-1.5-flash"
        model = genai.GenerativeModel(model_name)
        
        response = model.generate_content(prompt)
        return response.text
    
    def call_custom_api(self, prompt):
        """Placeholder for custom API call"""
        self.log_status("Attempting to call custom API...")
        # In a real implementation, you would use 'requests' here.
        # This is a placeholder for demonstration purposes.
        raise NotImplementedError("Custom API functionality is not implemented in this script.")
    
    def parse_text_suggestions(self, text):
        """Parse plain text suggestions if JSON fails"""
        return {
            'missing_keywords': re.findall(r'keyword[s]?:\s*([^\n]+)', text, re.I),
            'technical_terms': re.findall(r'technical[^:]*:\s*([^\n]+)', text, re.I),
            'key_phrases': [],
            'suggestions': {
                'skills': [],
                'experience': [],
                'action_verbs': []
            }
        }
    
    def display_keyword_suggestions(self, keywords, immutable_fields):
        """Display keyword suggestions in a new window"""
        suggest_window = tk.Toplevel(self.root)
        suggest_window.title("Keyword Suggestions for Manual Optimization")
        suggest_window.geometry("900x700")
        
        # Main frame with scrollbar
        main_container = ttk.Frame(suggest_window, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(main_container, text="Resume Optimization Keywords", 
                         font=('Helvetica', 14, 'bold'))
        title.pack(pady=10)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Tab 1: Missing Keywords
        tab1 = ttk.Frame(notebook, padding="10")
        notebook.add(tab1, text="Missing Keywords")
        
        text1 = scrolledtext.ScrolledText(tab1, wrap=tk.WORD, height=20)
        text1.pack(fill=tk.BOTH, expand=True)
        text1.insert(1.0, "Keywords from JD that are NOT in your resume (Prioritize these!):\n\n")
        for kw in keywords.get('missing_keywords', []):
            text1.insert(tk.END, f"• {kw}\n")
        text1.config(state='disabled')
        
        # Tab 2: Technical Terms
        tab2 = ttk.Frame(notebook, padding="10")
        notebook.add(tab2, text="Technical Terms")
        
        text2 = scrolledtext.ScrolledText(tab2, wrap=tk.WORD, height=20)
        text2.pack(fill=tk.BOTH, expand=True)
        text2.insert(1.0, "Technical terms and acronyms to consider integrating:\n\n")
        for term in keywords.get('technical_terms', []):
            text2.insert(tk.END, f"• {term}\n")
        text2.config(state='disabled')
        
        # Tab 3: Key Phrases
        tab3 = ttk.Frame(notebook, padding="10")
        notebook.add(tab3, text="Key Phrases")
        
        text3 = scrolledtext.ScrolledText(tab3, wrap=tk.WORD, height=20)
        text3.pack(fill=tk.BOTH, expand=True)
        text3.insert(1.0, "Important phrases from the job description:\n\n")
        for phrase in keywords.get('key_phrases', []):
            text3.insert(tk.END, f"• {phrase}\n")
        text3.config(state='disabled')
        
        # Tab 4: Specific Suggestions
        tab4 = ttk.Frame(notebook, padding="10")
        notebook.add(tab4, text="Manual Tips & Verbs")
        
        text4 = scrolledtext.ScrolledText(tab4, wrap=tk.WORD, height=20)
        text4.pack(fill=tk.BOTH, expand=True)
        
        suggestions = keywords.get('suggestions', {})
        
        text4.insert(tk.END, "=== SKILLS SECTION (to add) ===\n")
        text4.insert(tk.END, "Consider adding these skills to your dedicated skills list:\n\n")
        for skill in suggestions.get('skills', []):
            text4.insert(tk.END, f"• {skill}\n")
        
        text4.insert(tk.END, "\n\n=== EXPERIENCE PHRASES (to integrate) ===\n")
        text4.insert(tk.END, "Use these phrases when updating your job bullet points:\n\n")
        for exp in suggestions.get('experience', []):
            text4.insert(tk.END, f"• {exp}\n")
        
        text4.insert(tk.END, "\n\n=== ACTION VERBS (to start bullet points) ===\n")
        text4.insert(tk.END, "Ensure your accomplishment bullet points start with strong action verbs:\n\n")
        for verb in suggestions.get('action_verbs', []):
            text4.insert(tk.END, f"• {verb}\n")
        
        if 'placement_tips' in keywords:
            text4.insert(tk.END, "\n\n=== AI PLACEMENT TIPS ===\n\n")
            for tip in keywords['placement_tips']:
                text4.insert(tk.END, f"• {tip}\n")
        
        text4.config(state='disabled')
        
        # Tab 5: Protected Fields
        tab5 = ttk.Frame(notebook, padding="10")
        notebook.add(tab5, text="Protected Info")
        
        text5 = scrolledtext.ScrolledText(tab5, wrap=tk.WORD, height=20)
        text5.pack(fill=tk.BOTH, expand=True)
        text5.insert(1.0, "These fields were extracted and should remain exactly as they are:\n\n")
        for field, value in immutable_fields.items():
            text5.insert(tk.END, f"{field.upper()}: {value}\n")
        text5.config(state='disabled')
        
        # Export button
        export_btn = ttk.Button(main_container, text="Export Suggestions to File",
                               command=lambda: self.export_suggestions(keywords))
        export_btn.pack(pady=10)
        
        self.log_status("✓ Keyword suggestions generated successfully!")
    
    def export_suggestions(self, keywords):
        """Export suggestions to a text file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Keyword Suggestions"
        )
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("ATS KEYWORD SUGGESTIONS FOR MANUAL OPTIMIZATION\n")
                f.write("=" * 50 + "\n\n")
                
                f.write("MISSING KEYWORDS (Prioritize):\n")
                for kw in keywords.get('missing_keywords', []):
                    f.write(f"• {kw}\n")
                
                f.write("\n\nTECHNICAL TERMS:\n")
                for term in keywords.get('technical_terms', []):
                    f.write(f"• {term}\n")
                
                f.write("\n\nKEY PHRASES:\n")
                for phrase in keywords.get('key_phrases', []):
                    f.write(f"• {phrase}\n")
                
                suggestions = keywords.get('suggestions', {})
                
                f.write("\n\nSKILLS TO ADD:\n")
                for skill in suggestions.get('skills', []):
                    f.write(f"• {skill}\n")
                
                f.write("\n\nEXPERIENCE PHRASES:\n")
                for exp in suggestions.get('experience', []):
                    f.write(f"• {exp}\n")
                
                f.write("\n\nACTION VERBS:\n")
                for verb in suggestions.get('action_verbs', []):
                    f.write(f"• {verb}\n")
                
                if 'placement_tips' in keywords:
                    f.write("\n\nAI PLACEMENT TIPS:\n")
                    for tip in keywords['placement_tips']:
                        f.write(f"• {tip}\n")
            
            self.log_status(f"✓ Suggestions exported to: {file_path}")
            messagebox.showinfo("Success", f"Suggestions saved to:\n{file_path}")
    
    # REMOVED: auto_apply_keywords method
    # REMOVED: apply_keywords_to_resume method
    # REMOVED: apply_keywords_to_latex method
    # REMOVED: apply_keywords_to_text method
    # REMOVED: save_modified_resume method
    
    def clear_all(self):
        self.resume_file = None
        self.resume_content = ""
        self.resume_format = None
        self.file_label.config(text="No file selected", foreground="gray")
        self.resume_preview.delete(1.0, tk.END)
        self.jd_text_widget.delete(1.0, tk.END)
        self.status_text.config(state='normal')
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state='disabled')
        self.log_status("Cleared all data")

def main():
    root = tk.Tk()
    app = ATSKeywordSuggestorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
