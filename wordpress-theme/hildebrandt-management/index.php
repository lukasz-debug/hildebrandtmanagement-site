<?php
get_header();
?>

<main class="hm-main">
  <section class="hm-section hm-hero">
    <h1 class="hm-h1"><?php bloginfo('name'); ?></h1>
    <p class="hm-lead hm-text"><?php bloginfo('description'); ?></p>
  </section>

  <section class="hm-section">
    <?php if (have_posts()) : ?>
      <?php while (have_posts()) : the_post(); ?>
        <article>
          <h2 class="hm-h2"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
          <div class="hm-text"><?php the_excerpt(); ?></div>
        </article>
      <?php endwhile; ?>
    <?php else : ?>
      <p class="hm-text">Brak treści do wyświetlenia.</p>
    <?php endif; ?>
  </section>
</main>

<?php
get_footer();
