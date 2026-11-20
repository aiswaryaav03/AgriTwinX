import pptx

prs = pptx.Presentation('AgriTwinX_Final_Project_Review.pptx')
for i, slide in enumerate(prs.slides):
    print(f"=== SLIDE {i+1} ===")
    for s in slide.shapes:
        if s.has_text_frame:
            tf = s.text_frame
            total_text = ' '.join(p.text for p in tf.paragraphs if p.text.strip())
            if len(total_text) > 0:
                h_in = s.height / 914400
                w_in = s.width / 914400
                font_sizes = []
                for p in tf.paragraphs:
                    if p.font and p.font.size:
                        font_sizes.append(p.font.size.pt)
                    for r in p.runs:
                        if r.font and r.font.size:
                            font_sizes.append(r.font.size.pt)
                min_fs = min(font_sizes) if font_sizes else 'N/A'
                max_fs = max(font_sizes) if font_sizes else 'N/A'
                print(f"   Shape: {s.name[:20]:20} | W:{w_in:5.2f} H:{h_in:5.2f} | Pars: {len(tf.paragraphs):2} | Pt: {min_fs}-{max_fs} | Len: {len(total_text):4} | {total_text[:45]}...")

