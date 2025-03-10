css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
.document-item {
    padding: 0.5rem;
    margin-bottom: 0.5rem;
    border-radius: 0.25rem;
    background-color: #2b313e;
    cursor: pointer;
}
.document-item:hover {
    background-color: #3c4250;
}
.file-structure {
    max-height: 300px;
    overflow-y: auto;
    padding: 0.5rem;
    background-color: #2b313e;
    border-radius: 0.25rem;
}
.directory {
    padding-left: 1rem;
    cursor: pointer;
}
.file {
    padding-left: 2rem;
    cursor: pointer;
}
.source-document {
    background-color: #2b313e;
    padding: 0.5rem;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
    border-radius: 0.25rem;
    font-size: 0.8rem;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''

file_structure_template = '''
<div class="file-structure">
    {{CONTENT}}
</div>
'''

directory_template = '''
<div class="directory" onclick="navigateToDirectory('{{PATH}}')">
    📁 {{NAME}}
</div>
'''

file_template = '''
<div class="file" onclick="openFile('{{PATH}}')">
    📄 {{NAME}}
</div>
'''

source_document_template = '''
<div class="source-document">
    <strong>Source:</strong> {{SOURCE}}
</div>
'''