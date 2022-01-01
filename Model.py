import pandas as pd
from nltk.tokenize import TweetTokenizer
tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,reduce_len=True)


class Search_class:
 
    def __init__(self):
        self.df = pd.read_csv('H:/4/Selected 3/Project/Books.csv')
        self.df = self.df.dropna(axis=0)
        self.df = pd.DataFrame(self.df)
    
    
    def search(self,question):
        Dict = {}
        print(self.df)
        tokens = tokenizer.tokenize(question)
    
        
        searchfortitle = ["مؤلفات","أعمال","كتب"]
        searchforauthor = ["مؤلف","كاتب","ناشر"]
        searchforph = ["منشورات","إصدارات"]
        searchforsizeandnofpages = ["مجلد","كتاب","مجلة"]
#        ما هي كتب او مؤلفات او اعمال (اسم الكاتب )
        if tokens[0] == "ما" and (tokens[1] in searchfortitle or tokens[2] in searchfortitle) and "دار" not in tokens:
            if tokens[1] in searchfortitle:
                auth = ""
                for token in tokens[2:]:
                    auth+= token
                    auth += " "
                auth = auth[0:len(auth)-1]
                titles = self.df['title'].where(self.df['Author'] == auth)
                links = self.df['linkforpdf'].where(self.df['Author'] == auth)
            else :
                auth = ""
                for token in tokens[3:]:
                    auth+= token
                    auth += " "
                auth = auth[0:len(auth)-1]
                titles = self.df['title'].where(self.df['Author'] == auth)
                links = self.df['linkforpdf'].where(self.df['Author'] == auth)
                
            titles = list(titles.dropna(axis=0))
            links = list(links.dropna(axis=0))
            Dict["type"] = ["اسم الكتاب"]
            Dict["data"] = {}
            for i in range(len(titles)):
                Dict["data"][titles[i]] = links[i]
           # return(Dict)
        # من هو مؤلف / كاتب / ناشر (اسم العمل)
        elif tokens[0] == "من" and (tokens[1] in searchforauthor or tokens[2] in searchforauthor):
            if tokens[1] in searchforauthor:
                title = ""
                for token in tokens[2:]:
                    title+= token
                    title+= " "
            else:
                title = ""
                for token in tokens[3:]:
                    title+=token
                    title+=" "
                    
            title = title[0:len(title)-1]
            Authors = self.df['Author'].where(self.df['title'] == title)
           # links = self.df['linkforpdf'].where(self.df['title'] == title)
            Authors = list(Authors.dropna(axis=0))
            #links = links.dropna(axis=0)  
            Dict["type"] = ["اسم الكاتب","اسم الكتاب"]
            Dict["data"] = {}
            if Authors:
                Dict["data"][Authors[0]] = title
                
           # return(Dict)
# ما / ما هي منشورات / إصدارات (دار النشر)؟
        elif tokens[0] == "ما" and (tokens[1] in searchforph or tokens[2] in searchforph) :
            house = ""
            if tokens[1] in searchforph:
                for token in tokens[2:]:
                    house+=token
                    house+=" "
            else:
                for token in tokens[3:]:
                    house+=token
                    house+=" "
             
            house = house[0:len(house)-1]
            titles = self.df['title'].where(self.df['publishing_house'] == house)
            links = self.df['linkforpdf'].where(self.df['publishing_house'] == house)
            titles = list(titles.dropna(axis=0))
            links = list(links.dropna(axis=0))  
            Dict["type"] = ["اسم الكتاب"]
            Dict["data"] = {}
            for i in range(len(titles)):
                Dict["data"][titles[i]] = links[i]
          #  return(Dict)

        #كم عدد مؤلفات محمود
        #كم مؤلفات محمود
            
        elif tokens[0] == "كم" and (tokens[1] in searchfortitle or tokens[2] in searchfortitle):
            auth = ""
            if tokens[1] in searchfortitle: 
                for token in tokens[2:]:
                    auth+= token
                    auth += " "
            elif tokens[1] == "عدد":
                for token in tokens[3:]:
                    auth+= token
                    auth += " "
            else:
                Dict["type"] = "Error"
                return(Dict )
            auth = auth[0:len(auth)-1]
            titles = self.df['title'].where(self.df['Author'] == auth)
                  
            titles = titles.dropna(axis=0)
            Dict["type"] = ["اسم الكاتب","عدد المؤلفات"]
            Dict["data"] = {}
            Dict["data"][auth] = len(titles)
           # return(Dict)
#كم عدد منشورات دار النشر
        elif tokens[0] == "كم" and (tokens[1] in searchforph or tokens[2] in searchforph):
            house = ""
            if tokens[1] in searchfortitle: 
                for token in tokens[2:]:
                    house+= token
                    house += " "
            elif tokens[1] == "عدد" :
                for token in tokens[3:]:
                    house+= token
                    house += " "
            else:
                Dict["type"] = "Error"
                return(Dict)
            house = house[0:len(house)-1]
            titles = self.df['title'].where(self.df['publishing_house'] == house)
                  
            titles = titles.dropna(axis=0)
            Dict["type"] = ["اسم دار النشر","عدد المنشورات"]
            Dict["data"] = {}
            if len(titles) != 0:
                Dict["data"][house] = len(titles)

           # return(Dict)
#كم عدد صفحات كتاب (اسم)
        elif tokens[0] == "كم" and tokens[1] == "عدد" and tokens[2] == "صفحات" :
            B_Name = ""
            
            for token in tokens[3:]:
                B_Name+= token
                B_Name += " "
            
            B_Name = B_Name[0:len(B_Name)-1]
            Number = self.df['Nofpages'].where(self.df['title'] == B_Name)
                  
            Number = list(Number.dropna(axis=0))
            Dict["type"] = ["اسم الكتاب","عدد الصفحات"]
            Dict["data"] = {}
            if Number :
                Dict["data"][B_Name] = int(Number[0])
            #return(Dict)
      #  ما / ماهو قسم كتاب / مجلة (اسم الكتاب) ؟
        elif tokens[0] == "ما" and (tokens[1] == "قسم" or tokens[2] =="قسم") :
            title = ""
            if tokens[1] == "قسم":
                for token in tokens[2:]:
                    title+=token
                    title+=" "
            else:
                for token in tokens[3:]:
                    title+=token
                    title+=" "
             
            title = title[0:len(title)-1]
            Section = self.df['Section'].where(self.df['title'] == title)
            Section = list(Section.dropna(axis=0))
            Dict["type"] = ["اسم الكتاب","القسم"]
            Dict["data"] = {}
            if Section:
                Dict["data"][title] = Section[0]

            #return(Dict)
        
        else:
            Dict["type"] = "Error"
           # return(Dict)
        return(Dict)  



    
    
    
    
    
    
    
    
    
    
    


















