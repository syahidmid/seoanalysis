import streamlit as st

class PromptGenerator:
    def __init__(self, prompt_name):
        self.prompt_name = prompt_name
        self.session_state = st.session_state.setdefault(prompt_name, {})

        if 'topic' not in self.session_state:
            self.session_state['topic'] = ''
        if 'length' not in self.session_state:
            self.session_state['length'] = 0
        if 'style' not in self.session_state:
            self.session_state['style'] = 'Casual'
        if 'reader_greeting' not in self.session_state:
            self.session_state['reader_greeting'] = 'Kamu'
        if 'primary_keyword' not in self.session_state:
            self.session_state['primary_keyword'] = ''
        if 'outline' not in self.session_state:
            self.session_state['outline'] = ''
        if 'references' not in self.session_state:
            self.session_state['references'] = ''

    def generate_prompt(self):
        topic = st.text_input("Topic:", value=self.session_state['topic'], key=f"{self.prompt_name}_topic")
        length = st.slider("Length:", min_value=0, max_value=2000, value=self.session_state.get('length', 500), key=f"{self.prompt_name}_length")
        style = st.selectbox("Style:", options=["Casual", "Formal"], index=0 if self.session_state['style'] == 'Casual' else 1, key=f"{self.prompt_name}_style")
        reader_greeting = st.selectbox("Sapaan ke pembaca:", options=["Kamu", "Anda"], index=0 if self.session_state['reader_greeting'] == 'Kamu' else 1, key=f"{self.prompt_name}_reader_greeting")
        primary_keyword = st.text_input("Primary keyword:", value=self.session_state['primary_keyword'], key=f"{self.prompt_name}_primary_keyword")
        outline = st.text_area("Outline:", value=self.session_state['outline'], key=f"{self.prompt_name}_outline")
        references = st.text_area('References: ', value=self.session_state['references'], key=f"{self.prompt_name}_references")

        if st.button("Generate"):
            prompt = self.generate_prompt_text(topic, length, style, reader_greeting, primary_keyword, outline, references)
            st.session_state[f"{self.prompt_name}_result"] = prompt

        if f"{self.prompt_name}_result" in st.session_state:
            st.success(f"{self.prompt_name} Prompt yang dihasilkan:")
            st.code(st.session_state[f"{self.prompt_name}_result"])

        # Update session state
        self.session_state['topic'] = topic
        self.session_state['length'] = length
        self.session_state['style'] = style
        self.session_state['reader_greeting'] = reader_greeting
        self.session_state['primary_keyword'] = primary_keyword
        self.session_state['outline'] = outline
        self.session_state['references'] = references

    def generate_prompt_text(self, topic, length, style, reader_greeting, primary_keyword, outline, references):
        prompt = f"Tolong buatkan artikel tentang {topic} dengan primary keyword {primary_keyword} sepanjang {length} kata."
        prompt += f"Gunakan gaya bahasa {style} dengan kata '{reader_greeting}' untuk menyebut pembaca. Perhatikan penempatan kata kunci, wajib disebut di awal kalimat dan body artikel."
        prompt += f"Baca dan pahami referensi di bawah ini, ambil intisarinya dan jadikan artikel yang benar-benar baru dengan diksi dan struktur kalimat yang sama sekali berbeda."
        prompt += f"\nPrimary keyword: {primary_keyword}."
        prompt += f"\nOutline: {outline}."
        prompt += f"\nReferences: {references}."
        return prompt


def main():
    prompt_generator_1 = PromptGenerator(prompt_name="Outline Based Writing")
    prompt_generator_2 = PromptGenerator(prompt_name="Prompt 2")

    st.title("🤖GPT Prompt Generators")
    st.write("This application generates SEO prompts based on user inputs, allowing for easy customization of topics, lengths, styles, and outlines. It provides a streamlined prompt generation process for SEO content creation🔥")

    prompt_choices = ["Outline Based Writing", "Prompt 2"]
    selected_prompt = st.selectbox("Select Prompt:", prompt_choices)

    if selected_prompt == "Outline Based Writing":
        st.subheader("Outline Based Writing")
        prompt_generator_1.generate_prompt()
    elif selected_prompt == "Prompt 2":
        st.subheader("Prompt 2")
        prompt_generator_2.generate_prompt()

if __name__ == "__main__":
    main()




