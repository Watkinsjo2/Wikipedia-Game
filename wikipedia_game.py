import sys, wikipedia


# Gets the corresponding page from a Wikipedia article title 
def getArticle(articleName):
    try:
        articlePage = wikipedia.WikipediaPage(articleName)

    except wikipedia.exceptions.DisambiguationError as e:
        print('\nDisambiguation Error: Article name is too broad')

    except wikipedia.exceptions.PageError as e:
        print('Article page not found, try a different name')

    return articlePage


# Uses recursion to print the shortest path to the target article
def getShortRoute(linkPath):
    if linkPath['parentArticle']:
        getShortRoute(linkPath['parentArticle'])
        print(', ', end='')
    print(linkPath['articleTitle'], end='')


def gameStart():
    print('wikipedia_game\n')
        
    # The page to begin the game from
    sourceArticle = getArticle(input('Choose an article to use as the starting page: '))
    print()
    # The page to end the game with
    targetArticle = getArticle(input('Choose an article to use as the target page: '))
   
   # A dictionary consisting of smaller dictionaries for the source and its linked pages
    ConnectedPages = {
        sourceArticle.title : {
            'articleTitle': sourceArticle.title,
            'lenFromSource': 0,
            'parentArticle': None
        }       
    }
        
    print('\nStarting the game from: ' + sourceArticle.title + ' to ' + targetArticle.title)
        
    # Adds the source article dictionary to a queue of link dictionaries
    linkQueue = [ConnectedPages[sourceArticle.title]]
        
    # A boolean whose value is based on whether the target article has been reached
    targetFound = False
        
    while not targetFound:
        currentArticle = linkQueue[0]
        del linkQueue[0]
        try:
            articleLinks = wikipedia.WikipediaPage(currentArticle['articleTitle']).links

            # Adds every link on article page to the ConnectedPages dictionary            
            for link in articleLinks:
                print('\t' + link)
                if link not in ConnectedPages:
                    ConnectedPages[link] = {
                        'articleTitle': link,
                        'lenFromSource': currentArticle['lenFromSource'] + 1,
                        'parentArticle': currentArticle
                    }
                    if link == targetArticle.title:
                        print('\nTarget Located: ' + targetArticle.title)
                        print('The shortest path is: ', end='')
                        getShortRoute(ConnectedPages[link])
                        print()
                        targetFound = True
                        sys.exit()
                    linkQueue.append(ConnectedPages[link])
                                                    
        except wikipedia.exceptions.DisambiguationError as e:
            # Disambiguation Page
            ConnectedPages[e.title] = {
                'articleTitle': e.title,
                'lenFromSource': linkQueue[0]['lenFromSource'] + 1,
                'parentArticle': linkQueue[0]
            }
            # Adds every link on disambiguation page to the ConnectedPages dictionary
            for option in e.options:
                if option not in ConnectedPages:
                    ConnectedPages[option] = {
                        'articleTitle': option,
                        'lenFromSource': currentArticle['lenFromSource'] + 2,
                        'parentArticle': ConnectedPages[e.title]
                    }
                    if option == targetArticle.title:
                        print('\nTarget Located: ' + option)
                        print('The shortest path is: ', end='')
                        getShortRoute(ConnectedPages[option])
                        print()
                        targetFound = True
                        sys.exit()
                    linkQueue.append(ConnectedPages[option])
                    
        except wikipedia.exceptions.PageError as e:
            # Skips over the item in the linkQueueueue if it results in a page error.
            print(currentArticle['articleTitle'] + ' was not found, and will be skipped.')
            
        except KeyboardInterrupt:
            print('Exiting')
            targetFound = True
            sys.exit()


gameStart()
